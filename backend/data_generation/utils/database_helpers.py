"""
Database Helper Utilities for TrendMart Data Generation

Provides utilities for:
- Database connection management
- Bulk insert operations
- Transaction handling
- Data validation and cleanup
- Performance optimization
"""

from app import create_app
from extensions import db
import sys
import os
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DatabaseHelper:
    # Database operations helper for data generation

    def __init__(self, app=None):
        self.app = app or create_app()

    @contextmanager
    def get_db_session(self):
        # Context manager for database sessions with automatic rollback on error
        with self.app.app_context():
            session = db.session
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"Database error: {e}")
                raise
            finally:
                session.close()

    def clear_all_data(self, confirm: bool = False):
        """
        Clear all data from database (USE WITH CAUTION!)

        Args:
            confirm: Must be True to actually clear data
        """
        if not confirm:
            print("Database clear cancelled - confirmation required")
            return False

        print("Clearing all data from database...")

        with self.get_db_session() as session:
            try:
                # Import all models to ensure they're registered
                from models.analytics import UserSession, ProductView
                from models.catalog import Review, Inventory, Product, Category
                from models.registration import Address, CustomerProfile, User
                from models.shopping import CartItem, Cart, OrderItem, Order
                from models.recommendation import Recommendation

                # Delete in reverse order of dependencies
                tables_to_clear = [
                    # Analytics data
                    ProductView, UserSession,

                    # Shopping data
                    CartItem, Cart, OrderItem, Order,

                    # Reviews and recommendations
                    Review, Recommendation,

                    # User data
                    Address, CustomerProfile, User,

                    # Product data
                    Inventory, Product, Category
                ]

                for table_model in tables_to_clear:
                    count = session.query(table_model).count()
                    if count > 0:
                        session.query(table_model).delete()
                        print(
                            f"Cleared {count} records from {table_model.__tablename__}")

                # Clear many-to-many relationship table
                session.execute(text("DELETE FROM product_categories"))
                print("Cleared product_categories relationships")

                session.commit()
                print("All data cleared successfully")
                return True

            except Exception as e:
                print(f"Error clearing data: {e}")
                raise

    def bulk_insert(self, objects: List[Any], batch_size: int = 1000):
        """
        Efficient bulk insert with batching

        Args:
            objects: List of SQLAlchemy model instances
            batch_size: Number of objects to insert per batch
        """
        if not objects:
            return

        total_objects = len(objects)
        print(
            f"Bulk inserting {total_objects} objects in batches of {batch_size}...")

        with self.get_db_session() as session:
            try:
                for i in range(0, total_objects, batch_size):
                    batch = objects[i:i + batch_size]
                    session.bulk_save_objects(batch)

                    # Progress indicator
                    processed = min(i + batch_size, total_objects)
                    progress = (processed / total_objects) * 100
                    print(
                        f"Progress: {processed}/{total_objects} ({progress:.1f}%)")

                session.commit()
                print(f"Successfully inserted {total_objects} objects")

            except Exception as e:
                print(f"Bulk insert failed: {e}")
                raise

    def validate_data_integrity(self):
        # Validate data integrity and relationships

        print("Validating data integrity...")

        with self.get_db_session() as session:
            try:
                # Import models
                from models.registration import User, CustomerProfile
                from models.catalog import Product, Category, Review
                from models.shopping import Cart, Order
                from models.analytics import UserSession, ProductView

                issues = []

                # Check user relationships
                users_without_profiles = session.query(User).filter(
                    ~User.id.in_(session.query(CustomerProfile.user_id))
                ).count()
                if users_without_profiles > 0:
                    issues.append(
                        f"{users_without_profiles} users without customer profiles")

                # Check product relationships
                products_without_inventory = session.execute(text("""
                    SELECT COUNT(*) FROM products p 
                    WHERE p.id NOT IN (SELECT product_id FROM inventory)
                """)).scalar()
                if products_without_inventory > 0:
                    issues.append(
                        f"⚠️  {products_without_inventory} products without inventory")

                # Check orphaned reviews
                orphaned_reviews = session.execute(text("""
                    SELECT COUNT(*) FROM reviews r 
                    WHERE r.user_id NOT IN (SELECT id FROM users) 
                    OR r.product_id NOT IN (SELECT id FROM products)
                """)).scalar()
                if orphaned_reviews > 0:
                    issues.append(f"⚠️  {orphaned_reviews} orphaned reviews")

                # Check cart consistency
                carts_without_users = session.execute(text("""
                    SELECT COUNT(*) FROM carts c 
                    WHERE c.user_id NOT IN (SELECT id FROM users)
                """)).scalar()
                if carts_without_users > 0:
                    issues.append(
                        f"{carts_without_users} carts without valid users")

                if issues:
                    print("Data integrity issues found:")
                    for issue in issues:
                        print(f"  {issue}")
                else:
                    print("Data integrity validation passed")

                return len(issues) == 0

            except Exception as e:
                print(f"Validation error: {e}")
                return False

    def get_database_stats(self) -> Dict[str, int]:
        # Get comprehensive database statistics

        with self.get_db_session() as session:
            try:
                # Import models
                from models.registration import User, CustomerProfile, Address
                from models.catalog import Product, Category, Review, Inventory
                from models.shopping import Cart, CartItem, Order, OrderItem
                from models.analytics import UserSession, ProductView
                from models.recommendation import Recommendation

                stats = {
                    'users': session.query(User).count(),
                    'customer_profiles': session.query(CustomerProfile).count(),
                    'addresses': session.query(Address).count(),
                    'products': session.query(Product).count(),
                    'categories': session.query(Category).count(),
                    'inventory_records': session.query(Inventory).count(),
                    'reviews': session.query(Review).count(),
                    'carts': session.query(Cart).count(),
                    'cart_items': session.query(CartItem).count(),
                    'orders': session.query(Order).count(),
                    'order_items': session.query(OrderItem).count(),
                    'user_sessions': session.query(UserSession).count(),
                    'product_views': session.query(ProductView).count(),
                    'recommendations': session.query(Recommendation).count()
                }

                return stats

            except Exception as e:
                print(f"Error getting database stats: {e}")
                return {}

    def optimize_database(self):
        # Optimize database performance (PostgreSQL specific)
        print("Optimizing database performance...")

        with self.get_db_session() as session:
            try:
                # Update table statistics for better query planning
                session.execute(text("ANALYZE;"))
                print("Updated table statistics")

                # Vacuum to reclaim space (if needed)
                session.execute(text("VACUUM;"))
                print("Vacuumed database")

                session.commit()
                print("Database optimization completed")

            except Exception as e:
                print(f" Optimization error: {e}")

    def create_indexes(self):
        # Create additional indexes for better query performance
        print("Creating performance indexes...")

        with self.get_db_session() as session:
            try:
                indexes = [
                    # User analytics indexes
                    "CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);",
                    "CREATE INDEX IF NOT EXISTS idx_product_views_user_id ON product_views(user_id);",
                    "CREATE INDEX IF NOT EXISTS idx_product_views_product_id ON product_views(product_id);",
                    "CREATE INDEX IF NOT EXISTS idx_product_views_viewed_at ON product_views(viewed_at);",

                    # Shopping indexes
                    "CREATE INDEX IF NOT EXISTS idx_cart_items_product_id ON cart_items(product_id);",
                    "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);",
                    "CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);",
                    "CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);",

                    # Review indexes
                    "CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id);",
                    "CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);",
                    "CREATE INDEX IF NOT EXISTS idx_reviews_created_on ON reviews(created_on);",

                    # Product indexes
                    "CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);",
                    "CREATE INDEX IF NOT EXISTS idx_products_times_click_on ON products(times_click_on);"
                ]

                for index_sql in indexes:
                    try:
                        session.execute(text(index_sql))
                        print(f"Created index")
                    except Exception as idx_error:
                        print(f"Index creation warning: {idx_error}")

                session.commit()
                print("Performance indexes created")

            except Exception as e:
                print(f"Index creation error: {e}")


class DataValidationHelper:
    # Helper class for data validation and quality checks

    @staticmethod
    def validate_email(email: str) -> bool:
        # Simple email validation
        return "@" in email and "." in email.split("@")[1]

    @staticmethod
    def validate_price(price: float) -> bool:
        # Validate product price
        return price > 0 and price < 100000  # Reasonable price range

    @staticmethod
    def validate_rating(rating: float) -> bool:
        # Validate review rating
        return 0 <= rating <= 5

    @staticmethod
    def validate_quantity(quantity: int) -> bool:
        # Validate inventory/cart quantity
        return quantity >= 0 and quantity < 10000


def test_database_connection():
    # Test database connection and basic operations

    print("Testing database connection...")

    try:
        helper = DatabaseHelper()

        with helper.get_db_session() as session:
            # Test basic query
            result = session.execute(text("SELECT 1")).scalar()
            if result == 1:
                print("Database connection successful")
                return True
            else:
                print("Database connection test failed")
                return False

    except Exception as e:
        print(f"Database connection error: {e}")
        return False


if __name__ == "__main__":
    # Test the database utilities
    if test_database_connection():
        helper = DatabaseHelper()
        stats = helper.get_database_stats()

        print("\nCurrent Database Stats:")
        for table, count in stats.items():
            print(f"  {table}: {count}")

    print("\nDatabase utilities ready!")
