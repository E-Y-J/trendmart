"""
User Generator for TrendMart

Generates realistic user accounts with:
- Diverse user profiles and demographics
- Different activity levels (high, medium, low)
- Realistic authentication data
- Customer profiles with addresses
"""

from config.sample_data_config import DATA_CONFIG
from models.registration import User, CustomerProfile, Address
import random
from faker import Faker
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from typing import List, Dict
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


fake = Faker()


class UserGenerator:
    def __init__(self):
        self.users = []
        self.profiles = []
        self.addresses = []

    def generate_users(self) -> List[User]:
        # Generate realistic user accounts
        print("Generating users...")

        user_config = DATA_CONFIG["users"]
        user_count = user_config["count"]
        roles = user_config["roles"]
        activity_levels = user_config["activity_levels"]

        users = []

        for i in range(user_count):
            # Determine user role
            role = random.choices(
                list(roles.keys()),
                weights=list(roles.values())
            )[0]

            # Determine activity level
            activity_level = random.choices(
                list(activity_levels.keys()),
                weights=list(activity_levels.values())
            )[0]

            # Generate user data
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"

            # Make sure email is unique
            while any(user.email == email for user in users):
                email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@{fake.domain_name()}"

            # Generate realistic login history
            created_date = fake.date_time_between(
                start_date='-2y', end_date='-1w')
            logins_count = self._generate_login_count(
                activity_level, created_date)
            last_login = self._generate_last_login(
                created_date, activity_level)

            user = User(
                email=email,
                # Same password for all test users
                password_hash=generate_password_hash("password123"),
                role=role,
                active=random.choice([True] * 95 + [False]
                                     * 5),  # 95% active users
                created_at=created_date,
                logins_count=logins_count,
                last_login_at=last_login,
                # Most users have few failed attempts
                failed_logins=random.randint(0, 3)
            )

            # Store activity level for behavior generation
            user._activity_level = activity_level  # Temporary attribute for later use

            users.append(user)

        self.users = users
        return users

    def generate_customer_profiles(self) -> List[CustomerProfile]:
        # Generate customer profiles for users
        print("Generating customer profiles...")

        if not self.users:
            raise ValueError("Users must be generated first!")

        profiles = []

        for user in self.users:
            if user.role == 'customer':
                profile = CustomerProfile(
                    user_id=user.id,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=fake.phone_number(),
                    date_of_birth=fake.date_of_birth(
                        minimum_age=18, maximum_age=80),
                    gender=random.choice(['M', 'F', 'Other']),
                    # Preferences that will help with recommendations
                    preferred_categories=self._generate_category_preferences(),
                    newsletter_subscribed=random.choice([True, False]),
                    loyalty_points=random.randint(
                        0, 5000) if random.random() < 0.6 else 0
                )
                profiles.append(profile)

        self.profiles = profiles
        return profiles

    def generate_addresses(self) -> List[Address]:
        # Generate addresses for customer profiles
        print("Generating addresses...")

        if not self.profiles:
            raise ValueError("Customer profiles must be generated first!")

        addresses = []

        for profile in self.profiles:
            # Each customer gets 1-3 addresses
            address_count = random.choices(
                [1, 2, 3], weights=[0.6, 0.3, 0.1])[0]

            for i in range(address_count):
                is_primary = (i == 0)  # First address is primary

                address = Address(
                    customer_profile_id=profile.id,
                    address_type=random.choice(['home', 'work', 'other']),
                    is_primary=is_primary,
                    first_name=profile.first_name,
                    last_name=profile.last_name,
                    company=fake.company() if random.random() < 0.3 else None,
                    address_line_1=fake.street_address(),
                    address_line_2=fake.secondary_address() if random.random() < 0.3 else None,
                    city=fake.city(),
                    state_province=fake.state(),
                    postal_code=fake.zipcode(),
                    country=fake.country_code(),
                    phone=fake.phone_number()
                )
                addresses.append(address)

        self.addresses = addresses
        return addresses

    def _generate_login_count(self, activity_level: str, created_date: datetime) -> int:
        # Generate realistic login count based on activity level and account age
        days_since_creation = (datetime.utcnow() - created_date).days

        if activity_level == "high":
            avg_logins_per_week = random.uniform(4, 7)
        elif activity_level == "medium":
            avg_logins_per_week = random.uniform(1, 3)
        else:  # low
            avg_logins_per_week = random.uniform(0.2, 1)

        weeks_since_creation = days_since_creation / 7
        estimated_logins = int(avg_logins_per_week * weeks_since_creation)

        # Add some randomness
        return max(1, estimated_logins + random.randint(-10, 10))

    def _generate_last_login(self, created_date: datetime, activity_level: str) -> datetime:
        # Generate realistic last login based on activity level
        now = datetime.utcnow()

        if activity_level == "high":
            # High activity users logged in recently
            days_ago = random.randint(0, 7)
        elif activity_level == "medium":
            # Medium activity users logged in within last month
            days_ago = random.randint(1, 30)
        else:  # low
            # Low activity users might not have logged in for a while
            days_ago = random.randint(7, 180)

        last_login = now - timedelta(days=days_ago)

        # Make sure last login is after account creation
        return max(created_date, last_login)

    def _generate_category_preferences(self) -> str:
        # Generate category preferences for personalization
        categories = [cat["name"] for cat in DATA_CONFIG["categories"]]

        # Users typically prefer 2-4 categories
        preferred_count = random.randint(2, 4)
        preferred = random.sample(categories, preferred_count)

        return ", ".join(preferred)


def generate_user_data():
    # Main function to generate all user-related data
    generator = UserGenerator()

    # Generate in correct order
    users = generator.generate_users()
    profiles = generator.generate_customer_profiles()
    addresses = generator.generate_addresses()

    return {
        "users": users,
        "profiles": profiles,
        "addresses": addresses
    }


if __name__ == "__main__":
    # Test the generator
    data = generate_user_data()
    print(f"Generated {len(data['users'])} users")
    print(f"Generated {len(data['profiles'])} customer profiles")
    print(f"Generated {len(data['addresses'])} addresses")
