"""
Shopping Generator for TrendMart

Generates realistic shopping behavior data including:
- Shopping carts with items
- Completed orders and order items
- Realistic purchase patterns and conversion rates
- Cart abandonment scenarios
"""

from config.sample_data_config import DATA_CONFIG
from models.shopping import Cart, CartItem, Order, OrderItem
import random
from faker import Faker
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


fake = Faker()


class ShoppingGenerator:
    def __init__(self, users: List, products: List):
        self.users = users
        self.products = products
        self.carts = []
        self.cart_items = []
        self.orders = []
        self.order_items = []

    def generate_shopping_carts(self) -> Tuple[List[Cart], List[CartItem]]:
        # Generate shopping carts and cart items for users
        print("Generating shopping carts...")

        carts = []
        cart_items = []

        # Each user gets one cart (some empty, some with items, some abandoned)
        for user in self.users:
            activity_level = getattr(user, '_activity_level', 'medium')

            # Create cart for user
            cart_created = fake.date_time_between(
                start_date=user.created_at,
                end_date=datetime.utcnow()
            )

            cart = Cart(
                user_id=user.id,
                cart_created_at=cart_created,
                abandoned_flag=False,  # Will be updated based on items
                last_updated_at=cart_created
            )

            # Determine if user has items in cart
            has_cart_items = self._should_have_cart_items(activity_level)

            if has_cart_items:
                items, last_update = self._generate_cart_items(
                    user, cart, cart_created)
                cart_items.extend(items)
                cart.last_updated_at = last_update

                # Determine if cart is abandoned (items added but no recent activity)
                days_since_update = (datetime.utcnow() - last_update).days
                # Abandoned if no activity for 7+ days
                cart.abandoned_flag = days_since_update > 7

            carts.append(cart)

        self.carts = carts
        self.cart_items = cart_items
        return carts, cart_items

    def generate_orders(self) -> Tuple[List[Order], List[OrderItem]]:
        # Generate completed orders and order items
        print("Generating orders and order items...")

        orders = []
        order_items = []

        purchase_probability = DATA_CONFIG["behaviors"]["purchase_probability"]

        for user in self.users:
            activity_level = getattr(user, '_activity_level', 'medium')

            # Determine number of orders based on activity level
            if activity_level == 'high':
                max_orders = random.randint(2, 8)
            elif activity_level == 'medium':
                max_orders = random.randint(0, 3)
            else:  # low
                max_orders = random.randint(0, 1)

            # Generate orders for this user
            user_orders = self._generate_user_orders(user, max_orders)
            orders.extend(user_orders)

            # Generate order items for each order
            for order in user_orders:
                items = self._generate_order_items(user, order)
                order_items.extend(items)

        self.orders = orders
        self.order_items = order_items
        return orders, order_items

    def _should_have_cart_items(self, activity_level: str) -> bool:
        # Determine if user should have items in their cart
        probabilities = {
            'high': 0.7,    # 70% of high-activity users have cart items
            'medium': 0.4,  # 40% of medium-activity users have cart items
            'low': 0.15     # 15% of low-activity users have cart items
        }
        return random.random() < probabilities.get(activity_level, 0.3)

    def _generate_cart_items(self, user, cart, cart_created: datetime) -> Tuple[List[CartItem], datetime]:
        # Generate items for a user's cart
        cart_items = []

        # Number of items in cart (realistic distribution)
        item_count = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8],
            weights=[30, 25, 20, 10, 8, 4, 2, 1]  # Most carts have 1-3 items
        )[0]

        added_products = set()
        last_update = cart_created

        for i in range(item_count):
            # Select product (prefer products from user's preferred categories)
            product = self._select_product_for_user(user, added_products)
            if not product:
                break

            added_products.add(product.id)

            # When was this item added? (spread over time since cart creation)
            if i == 0:
                added_at = cart_created
            else:
                max_days_later = min(
                    30, (datetime.utcnow() - cart_created).days)
                days_later = random.randint(0, max(1, max_days_later))
                added_at = cart_created + timedelta(days=days_later)

            last_update = max(last_update, added_at)

            # Realistic quantity (most items are quantity 1)
            quantity = random.choices(
                [1, 2, 3, 4, 5], weights=[70, 15, 8, 4, 3])[0]

            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.price,
                added_at=added_at
            )

            cart_items.append(cart_item)

        return cart_items, last_update

    def _generate_user_orders(self, user, max_orders: int) -> List[Order]:
        # Generate orders for a specific user
        orders = []

        account_lifetime_days = (datetime.utcnow() - user.created_at).days
        if account_lifetime_days < 1:
            return orders

        for i in range(max_orders):
            # Spread orders over user's account lifetime
            days_after_creation = random.randint(
                1, max(1, account_lifetime_days))
            order_date = user.created_at + timedelta(days=days_after_creation)

            # Don't create future orders
            if order_date > datetime.utcnow():
                continue

            # Order status (most are completed)
            status = random.choices(
                ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
                weights=[5, 10, 15, 65, 5]  # 65% delivered
            )[0]

            # Shipping method
            shipping_method = random.choices(
                ['standard', 'express', 'overnight', 'pickup'],
                weights=[60, 25, 10, 5]
            )[0]

            order = Order(
                user_id=user.id,
                order_date=order_date,
                status=status,
                total_amount=0.0,  # Will be calculated when items are added
                shipping_address=fake.address(),
                billing_address=fake.address(),
                payment_method=random.choice(
                    ['credit_card', 'debit_card', 'paypal', 'apple_pay']),
                shipping_method=shipping_method,
                order_notes=fake.sentence() if random.random() < 0.2 else None,
                tracking_number=fake.uuid4() if status in [
                    'shipped', 'delivered'] else None
            )

            orders.append(order)

        return orders

    def _generate_order_items(self, user, order: Order) -> List[OrderItem]:
        # Generate items for a specific order
        order_items = []

        # Number of items in order (orders typically have more items than carts)
        item_count = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            weights=[20, 25, 20, 15, 10, 5, 3, 1, 0.5, 0.5]
        )[0]

        added_products = set()
        total_amount = 0.0

        for i in range(item_count):
            product = self._select_product_for_user(user, added_products)
            if not product:
                break

            added_products.add(product.id)

            # Realistic quantity
            quantity = random.choices(
                [1, 2, 3, 4, 5], weights=[60, 20, 10, 6, 4])[0]
            unit_price = product.price

            # Small chance of discount
            if random.random() < 0.1:  # 10% chance of discount
                discount_percent = random.uniform(0.05, 0.3)  # 5-30% off
                unit_price = round(unit_price * (1 - discount_percent), 2)

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                discount_amount=max(0, product.price - unit_price) * quantity
            )

            total_amount += unit_price * quantity
            order_items.append(order_item)

        # Update order total
        order.total_amount = round(total_amount, 2)

        return order_items

    def _select_product_for_user(self, user, excluded_products: set):
        # Select a product for a user based on their preferences
        available_products = [
            p for p in self.products if p.id not in excluded_products]

        if not available_products:
            return None

        # Get user's preferred categories (simplified - would come from profile in real app)
        activity_level = getattr(user, '_activity_level', 'medium')

        # High-activity users have more specific preferences
        if activity_level == 'high' and random.random() < 0.7:
            # Try to find products in preferred categories
            all_categories = [cat["name"] for cat in DATA_CONFIG["categories"]]
            preferred_categories = random.sample(
                all_categories, k=random.randint(2, 4))

            preferred_products = [
                p for p in available_products
                if any(cat.name in preferred_categories for cat in p.categories)
            ]

            if preferred_products:
                return random.choice(preferred_products)

        # Random selection
        return random.choice(available_products)


def generate_shopping_data(users: List, products: List):
    # Main function to generate all shopping data
    generator = ShoppingGenerator(users, products)

    # Generate in correct order
    carts, cart_items = generator.generate_shopping_carts()
    orders, order_items = generator.generate_orders()

    return {
        "carts": carts,
        "cart_items": cart_items,
        "orders": orders,
        "order_items": order_items
    }


if __name__ == "__main__":
    # This would need actual user and product data to test
    print("Shopping generator ready. Run from main script with user and product data.")
