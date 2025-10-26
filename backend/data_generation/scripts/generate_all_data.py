"""
Master Data Generation Script for TrendMart

This script orchestrates all data generators and populates the database
with realistic sample data for the recommendation system.

Usage:
    cd backend
    python data_generation/scripts/generate_all_data.py
"""

from data_generation.generators.behavior_generator import generate_behavior_data
from data_generation.generators.user_generator import generate_user_data
from data_generation.generators.product_generator import generate_catalog_data
from data_generation.generators.shopping_generator import generate_shopping_data
from data_generation.utils.database_helpers import DatabaseHelper, test_database_connection
from extensions import db
from app import create_app
import sys
import os
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)


class DataGenerationOrchestrator:
    def __init__(self, app):
        self.app = app
        self.generated_data = {}
        self.db_helper = DatabaseHelper(app)

    def clear_existing_data(self):
        """Clear existing sample data using database helper"""
        return self.db_helper.clear_all_data(confirm=True)

    def generate_and_save_catalog(self):
        # Generate and save categories, products, and inventory
        print("\n STEP 1: Generating Catalog Data")
        print("=" * 50)

        catalog_data = generate_catalog_data()

        with self.app.app_context():
            try:
                # Save categories first
                print("Saving categories...")
                for category in catalog_data["categories"]:
                    db.session.add(category)
                db.session.flush()  # Get IDs for relationships

                # Save products with category relationships
                print("Saving products...")
                for product in catalog_data["products"]:
                    db.session.add(product)
                db.session.flush()  # Get product IDs

                # Save inventory
                print("Saving inventory...")
                for inventory in catalog_data["inventory"]:
                    # Update product_id to match the saved product
                    matching_product = next(
                        p for p in catalog_data["products"] if p.sku == inventory.product.sku)
                    inventory.product_id = matching_product.id
                    db.session.add(inventory)

                db.session.commit()

                # Store for next steps
                self.generated_data['categories'] = catalog_data["categories"]
                self.generated_data['products'] = catalog_data["products"]

                print(f"Saved {len(catalog_data['categories'])} categories")
                print(f"Saved {len(catalog_data['products'])} products")
                print(
                    f"Saved {len(catalog_data['inventory'])} inventory records")

            except Exception as e:
                db.session.rollback()
                print(f"Error saving catalog data: {e}")
                raise

    def generate_and_save_users(self):
        # Generate and save users, profiles, and addresses
        print("\nSTEP 2: Generating User Data")
        print("=" * 50)

        user_data = generate_user_data()

        with self.app.app_context():
            try:
                # Save users first
                print("Saving users...")
                for user in user_data["users"]:
                    db.session.add(user)
                db.session.flush()  # Get user IDs

                # Save customer profiles
                print("Saving customer profiles...")
                for profile in user_data["profiles"]:
                    # Link to saved user
                    matching_user = next(
                        u for u in user_data["users"] if u.email == profile.user.email)
                    profile.user_id = matching_user.id
                    db.session.add(profile)
                db.session.flush()  # Get profile IDs

                # Save addresses
                print("Saving addresses...")
                for address in user_data["addresses"]:
                    # Link to saved profile
                    matching_profile = next(
                        p for p in user_data["profiles"] if p.user_id == address.customer_profile.user_id)
                    address.customer_profile_id = matching_profile.id
                    db.session.add(address)

                db.session.commit()

                # Store for next steps
                self.generated_data['users'] = user_data["users"]

                print(f"Saved {len(user_data['users'])} users")
                print(f"Saved {len(user_data['profiles'])} customer profiles")
                print(f"Saved {len(user_data['addresses'])} addresses")

            except Exception as e:
                db.session.rollback()
                print(f"Error saving user data: {e}")
                raise

    def generate_and_save_behaviors(self):
        # Generate and save user behaviors (sessions, views, reviews)
        print("\nSTEP 3: Generating Behavior Data")
        print("=" * 50)

        # Get fresh data from database with proper IDs
        with self.app.app_context():
            from models.registration import User
            from models.catalog import Product

            users = db.session.query(User).all()
            products = db.session.query(Product).all()

            print(
                f"Generating behaviors for {len(users)} users and {len(products)} products...")

            behavior_data = generate_behavior_data(users, products)

            try:
                # Save sessions first
                print("Saving user sessions...")
                for session in behavior_data["sessions"]:
                    db.session.add(session)
                db.session.flush()  # Get session IDs

                # Save product views
                print("Saving product views...")
                for view in behavior_data["views"]:
                    # Link to saved session
                    matching_session = next(s for s in behavior_data["sessions"]
                                            if s.user_id == view.user_id and
                                            abs((s.session_start - view.viewed_at).total_seconds()) < 3600)
                    view.session_id = matching_session.id
                    db.session.add(view)

                # Save reviews
                print("Saving reviews...")
                for review in behavior_data["reviews"]:
                    db.session.add(review)

                db.session.commit()

                print(f"Saved {len(behavior_data['sessions'])} user sessions")
                print(f"Saved {len(behavior_data['views'])} product views")
                print(f"Saved {len(behavior_data['reviews'])} reviews")

            except Exception as e:
                db.session.rollback()
                print(f"❌ Error saving behavior data: {e}")
                raise

    def generate_and_save_shopping(self):
        """Generate and save shopping data (carts, orders)"""
        print("\n🛒 STEP 4: Generating Shopping Data")
        print("=" * 50)

        # Get fresh data from database with proper IDs
        with self.app.app_context():
            from models.registration import User
            from models.catalog import Product

            users = db.session.query(User).all()
            products = db.session.query(Product).all()

            print(
                f"📊 Generating shopping data for {len(users)} users and {len(products)} products...")

            shopping_data = generate_shopping_data(users, products)

            try:
                # Save carts first
                print("💾 Saving shopping carts...")
                for cart in shopping_data["carts"]:
                    db.session.add(cart)
                db.session.flush()  # Get cart IDs

                # Save cart items
                print("💾 Saving cart items...")
                for cart_item in shopping_data["cart_items"]:
                    # Link to saved cart
                    matching_cart = next(
                        c for c in shopping_data["carts"] if c.user_id == cart_item.cart.user_id)
                    cart_item.cart_id = matching_cart.id
                    db.session.add(cart_item)

                # Save orders
                print("💾 Saving orders...")
                for order in shopping_data["orders"]:
                    db.session.add(order)
                db.session.flush()  # Get order IDs

                # Save order items
                print("💾 Saving order items...")
                for order_item in shopping_data["order_items"]:
                    # Link to saved order
                    matching_order = next(o for o in shopping_data["orders"]
                                          if o.user_id == order_item.order.user_id and
                                          abs((o.order_date - order_item.order.order_date).total_seconds()) < 60)
                    order_item.order_id = matching_order.id
                    db.session.add(order_item)

                db.session.commit()

                print(f"✅ Saved {len(shopping_data['carts'])} shopping carts")
                print(f"✅ Saved {len(shopping_data['cart_items'])} cart items")
                print(f"✅ Saved {len(shopping_data['orders'])} orders")
                print(
                    f"✅ Saved {len(shopping_data['order_items'])} order items")

            except Exception as e:
                db.session.rollback()
                print(f"❌ Error saving shopping data: {e}")
                raise

    def validate_and_optimize_database(self):
        """Validate data integrity and optimize database performance"""
        print("\n🔍 STEP 5: Validation & Optimization")
        print("=" * 50)

        # Validate data integrity
        is_valid = self.db_helper.validate_data_integrity()

        if is_valid:
            print("✅ Data integrity validation passed")
        else:
            print("⚠️  Data integrity issues detected (see details above)")

        # Create performance indexes
        self.db_helper.create_indexes()

        # Optimize database
        self.db_helper.optimize_database()

    def generate_summary_stats(self):
        # Generate and display summary statistics
        print("\nGENERATION SUMMARY")
        print("=" * 50)

        with self.app.app_context():
            from models.registration import User
            from models.catalog import Product, Category, Review
            from models.analytics import UserSession, ProductView
            from models.shopping import Cart, CartItem, Order, OrderItem

            # Get counts
            user_count = db.session.query(User).count()
            product_count = db.session.query(Product).count()
            category_count = db.session.query(Category).count()
            session_count = db.session.query(UserSession).count()
            view_count = db.session.query(ProductView).count()
            review_count = db.session.query(Review).count()
            cart_count = db.session.query(Cart).count()
            cart_item_count = db.session.query(CartItem).count()
            order_count = db.session.query(Order).count()
            order_item_count = db.session.query(OrderItem).count()

            # Calculate averages
            avg_sessions_per_user = session_count / user_count if user_count > 0 else 0
            avg_views_per_user = view_count / user_count if user_count > 0 else 0
            avg_reviews_per_product = review_count / \
                product_count if product_count > 0 else 0
            avg_cart_items_per_cart = cart_item_count / cart_count if cart_count > 0 else 0
            avg_orders_per_user = order_count / user_count if user_count > 0 else 0
            avg_order_items_per_order = order_item_count / \
                order_count if order_count > 0 else 0

            print(f"👥 Users: {user_count}")
            print(f"📦 Products: {product_count}")
            print(f"🏷️ Categories: {category_count}")
            print(
                f"🔍 Sessions: {session_count} (avg: {avg_sessions_per_user:.1f} per user)")
            print(
                f"👀 Product Views: {view_count} (avg: {avg_views_per_user:.1f} per user)")
            print(
                f"⭐ Reviews: {review_count} (avg: {avg_reviews_per_product:.1f} per product)")
            print(
                f"🛒 Shopping Carts: {cart_count} (avg: {avg_cart_items_per_cart:.1f} items per cart)")
            print(
                f"📋 Orders: {order_count} (avg: {avg_orders_per_user:.1f} per user)")
            print(
                f"📦 Order Items: {order_item_count} (avg: {avg_order_items_per_order:.1f} per order)")

            # Get most popular products
            print(f"\nMost Popular Products:")
            popular_products = db.session.query(Product).order_by(
                Product.times_click_on.desc()).limit(5).all()
            for i, product in enumerate(popular_products, 1):
                print(f"  {i}. {product.name} ({product.times_click_on} views)")

    def run_full_generation(self, clear_existing=True):
        # Run the complete data generation process
        start_time = datetime.now()

        print("TRENDMART DATA GENERATION STARTED")
        print("=" * 60)
        print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            if clear_existing:
                self.clear_existing_data()

            self.generate_and_save_catalog()
            self.generate_and_save_users()
            self.generate_and_save_behaviors()
            self.generate_and_save_shopping()
            self.validate_and_optimize_database()
            self.generate_summary_stats()

            end_time = datetime.now()
            duration = end_time - start_time

            print(f"\nDATA GENERATION COMPLETED SUCCESSFULLY!")
            print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Total duration: {duration.total_seconds():.1f} seconds")
            print(
                f"\nYour TrendMart database is now ready for recommendation system development!")

        except Exception as e:
            print(f"\nDATA GENERATION FAILED: {e}")
            raise


def main():
    """Main entry point"""
    print("🚀 TRENDMART DATA GENERATION STARTING...")
    print("=" * 60)

    # Test database connection first
    if not test_database_connection():
        print("❌ Database connection failed. Please check your configuration.")
        print("💡 Make sure PostgreSQL is running: docker-compose up -d database")
        return

    print("Initializing Flask app...")
    app = create_app()

    orchestrator = DataGenerationOrchestrator(app)

    # Ask user if they want to clear existing data
    clear_data = input(
        "\n🤔 Clear existing data before generation? (y/N): ").lower().strip()
    should_clear = clear_data in ['y', 'yes']

    orchestrator.run_full_generation(clear_existing=should_clear)


if __name__ == "__main__":
    main()
