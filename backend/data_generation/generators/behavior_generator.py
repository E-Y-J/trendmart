"""
Behavior Generator for TrendMart

Generates realistic user behavior data including:
- User sessions with browsing patterns
- Product views and interactions  
- Reviews and ratings
- Realistic behavioral patterns for recommendations
"""

from config.sample_data_config import DATA_CONFIG
from models.recommendation import Recommendation
from models.catalog import Review
from models.analytics import UserSession, ProductView
import random
from faker import Faker
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import json
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


fake = Faker()


class BehaviorGenerator:
    def __init__(self, users: List, products: List):
        self.users = users
        self.products = products
        self.sessions = []
        self.product_views = []
        self.reviews = []
        self.user_preferences = {}  # Track what each user likes

    def generate_user_sessions(self) -> List[UserSession]:
        # Generate realistic user sessions with browsing patterns
        print("Generating user sessions...")

        sessions = []
        behavior_config = DATA_CONFIG["behaviors"]

        for user in self.users:
            activity_level = getattr(user, '_activity_level', 'medium')
            session_range = behavior_config["sessions_per_user"][activity_level]
            session_count = random.randint(*session_range)

            # Generate sessions spread over time since account creation
            user_sessions = self._generate_sessions_for_user(
                user, session_count)
            sessions.extend(user_sessions)

        self.sessions = sessions
        return sessions

    def generate_product_views(self) -> List[ProductView]:
        # Generate product views during user sessions
        print("Generating product views...")

        if not self.sessions:
            raise ValueError("User sessions must be generated first!")

        product_views = []
        views_range = DATA_CONFIG["behaviors"]["views_per_session"]

        for session in self.sessions:
            view_count = random.randint(*views_range)
            session_views = self._generate_views_for_session(
                session, view_count)
            product_views.extend(session_views)

        self.product_views = product_views

        # Update product click counts
        self._update_product_click_counts()

        return product_views

    def generate_reviews(self) -> List[Review]:
        # Generate reviews based on product views and user behavior
        print("Generating reviews...")

        if not self.product_views:
            raise ValueError("Product views must be generated first!")

        reviews = []
        review_probability = DATA_CONFIG["behaviors"]["review_probability"]

        # Group views by user and product to avoid duplicate reviews
        user_product_views = {}
        for view in self.product_views:
            key = (view.user_id, view.product_id)
            if key not in user_product_views:
                user_product_views[key] = []
            user_product_views[key].append(view)

        for (user_id, product_id), views in user_product_views.items():
            # Only create review if user viewed product multiple times or spent significant time
            total_time = sum(view.time_spent or 0 for view in views)
            view_count = len(views)

            should_review = (
                random.random() < review_probability and
                # Multiple views or 5+ minutes
                (view_count >= 2 or total_time > 300)
            )

            if should_review:
                review = self._create_review(user_id, product_id, views)
                reviews.append(review)

        self.reviews = reviews
        return reviews

    def _generate_sessions_for_user(self, user, session_count: int) -> List[UserSession]:
        # Generate sessions for a specific user
        sessions = []
        account_age_days = (datetime.utcnow() - user.created_at).days

        for i in range(session_count):
            # Distribute sessions over the user's account lifetime
            days_ago = random.randint(0, max(1, account_age_days))
            session_start = datetime.utcnow() - timedelta(days=days_ago)
            session_start += timedelta(
                hours=random.randint(6, 23),
                minutes=random.randint(0, 59)
            )

            # Session duration based on activity level
            activity_level = getattr(user, '_activity_level', 'medium')
            if activity_level == 'high':
                duration_minutes = random.randint(15, 120)
            elif activity_level == 'medium':
                duration_minutes = random.randint(5, 45)
            else:  # low
                duration_minutes = random.randint(2, 15)

            session_end = session_start + timedelta(minutes=duration_minutes)

            session = UserSession(
                user_id=user.id,
                ip_address=fake.ipv4(),
                user_agent=fake.user_agent(),
                session_start=session_start,
                session_end=session_end,
                pages_visited=0,  # Will be updated when views are created
                click_path="",  # Will be updated with navigation path
                time_per_page=duration_minutes *
                60 / max(1, random.randint(2, 8))
            )

            sessions.append(session)

        return sessions

    def _generate_views_for_session(self, session: UserSession, view_count: int) -> List[ProductView]:
        # Generate product views for a specific session
        views = []
        user = next(u for u in self.users if u.id == session.user_id)

        # Get user's preferred categories for more realistic browsing
        user_preferences = self._get_user_category_preferences(user)

        session_duration = (session.session_end -
                            session.session_start).total_seconds()
        time_per_view = session_duration / view_count

        viewed_products = set()  # Avoid duplicate views in same session

        for i in range(view_count):
            # Choose product based on user preferences (70% of the time)
            if random.random() < 0.7 and user_preferences:
                preferred_category = random.choice(user_preferences)
                matching_products = [
                    p for p in self.products
                    if any(cat.name == preferred_category for cat in p.categories)
                    and p.id not in viewed_products
                ]

                if matching_products:
                    product = random.choice(matching_products)
                else:
                    product = random.choice(
                        [p for p in self.products if p.id not in viewed_products])
            else:
                # Random browsing
                available_products = [
                    p for p in self.products if p.id not in viewed_products]
                if not available_products:
                    break
                product = random.choice(available_products)

            viewed_products.add(product.id)

            # Calculate view time within session
            view_start = session.session_start + \
                timedelta(seconds=i * time_per_view)
            # 10 seconds to 1.5x average
            time_spent = random.randint(10, int(time_per_view * 1.5))

            view = ProductView(
                user_id=session.user_id,
                product_id=product.id,
                session_id=session.id,
                viewed_at=view_start,
                time_spent=time_spent,
                came_from=self._generate_referrer(),
                device_type=self._extract_device_type(session.user_agent)
            )

            views.append(view)

        # Update session with actual page count
        session.pages_visited = len(views)

        return views

    def _create_review(self, user_id: int, product_id: int, views: List[ProductView]) -> Review:
        # Create a realistic review based on user's viewing behavior
        # Rating influenced by time spent and user's general satisfaction
        total_time_spent = sum(view.time_spent or 0 for view in views)
        view_count = len(views)

        # Users who spend more time or return multiple times tend to rate higher
        base_rating = 3.0
        if total_time_spent > 300:  # 5+ minutes
            base_rating += 0.5
        if view_count >= 3:  # Multiple visits
            base_rating += 0.5

        # Add some randomness
        rating = base_rating + random.uniform(-1.0, 1.5)
        rating = max(1.0, min(5.0, rating))  # Clamp between 1-5
        rating = round(rating * 2) / 2  # Round to nearest 0.5

        # Generate review text based on rating
        if rating >= 4.5:
            title = random.choice([
                "Excellent product!", "Love it!", "Highly recommend!",
                "Perfect!", "Exceeded expectations!"
            ])
            comment = fake.paragraph(nb_sentences=random.randint(2, 4))
        elif rating >= 3.5:
            title = random.choice([
                "Good product", "Pretty good", "Satisfied",
                "Good value", "Does the job"
            ])
            comment = fake.paragraph(nb_sentences=random.randint(1, 3))
        elif rating >= 2.5:
            title = random.choice([
                "It's okay", "Average", "Could be better",
                "Mixed feelings", "Decent but not great"
            ])
            comment = fake.paragraph(nb_sentences=random.randint(1, 2))
        else:
            title = random.choice([
                "Disappointed", "Not worth it", "Poor quality",
                "Would not recommend", "Waste of money"
            ])
            comment = fake.paragraph(nb_sentences=1)

        # Review created shortly after last view
        last_view = max(views, key=lambda v: v.viewed_at)
        created_on = last_view.viewed_at + timedelta(
            hours=random.randint(1, 72)  # 1 hour to 3 days later
        )

        return Review(
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            title=title,
            comment=comment,
            created_on=created_on
        )

    def _get_user_category_preferences(self, user) -> List[str]:
        # Get user's preferred categories from their profile
        all_categories = [cat["name"] for cat in DATA_CONFIG["categories"]]

        activity_level = getattr(user, '_activity_level', 'medium')
        if activity_level == 'high':
            pref_count = random.randint(3, 5)
        elif activity_level == 'medium':
            pref_count = random.randint(2, 4)
        else:
            pref_count = random.randint(1, 3)

        return random.sample(all_categories, min(pref_count, len(all_categories)))

    def _update_product_click_counts(self):
        # Update times_click_on for products based on views
        product_clicks = {}
        for view in self.product_views:
            product_clicks[view.product_id] = product_clicks.get(
                view.product_id, 0) + 1

        for product in self.products:
            product.times_click_on = product_clicks.get(product.id, 0)

    def _generate_referrer(self) -> str:
        # Generate realistic referrer sources
        referrers = [
            "google.com", "facebook.com", "instagram.com", "twitter.com",
            "direct", "email", "pinterest.com", "youtube.com", "bing.com"
        ]
        return random.choice(referrers)

    def _extract_device_type(self, user_agent: str) -> str:
        # Extract device type from user agent string
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            return 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'tablet'
        else:
            return 'desktop'


def generate_behavior_data(users: List, products: List):
    # Main function to generate all behavior data
    generator = BehaviorGenerator(users, products)

    # Generate in correct order
    sessions = generator.generate_user_sessions()
    views = generator.generate_product_views()
    reviews = generator.generate_reviews()

    return {
        "sessions": sessions,
        "views": views,
        "reviews": reviews
    }


if __name__ == "__main__":
    # This would need actual user and product data to test
    print("Behavior generator ready. Run from main script with user and product data.")
