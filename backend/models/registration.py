from datetime import datetime
from extensions import db


class User(db.Model):
    """
    User Account Model

    Core authentication and account management model.
    Serves as the central entity for all user-related functionality.

    Attributes:
        id (int): Primary key, unique user identifier
        email (str): Unique email address for login and communication
        password_hash (str): Hashed password (never store plain text!)
        role (str): User role for authorization (customer, admin, etc.)
        active (bool): Account status flag, defaults to True
        created_at (datetime): Account creation timestamp

    Security Notes:
        - Passwords are always hashed, never stored in plain text
        - Email uniqueness enforced at database level
        - Active flag allows soft account deactivation
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    logins_count = db.Column(db.Integer, default=0, nullable=False)
    last_login_at = db.Column(db.DateTime)
    failed_logins = db.Column(db.Integer, default=0, nullable=False)

    # Relationships - User is the central hub for all user-related data
    # One-to-one: Each user has one customer profile
    customer_profile = db.relationship(
        'CustomerProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')

    # One-to-many: User can have multiple addresses
    addresses = db.relationship(
        'Address', back_populates='user', cascade='all, delete-orphan')

    # One-to-one: Each user has one active cart
    cart = db.relationship('Cart', back_populates='user',
                           uselist=False, cascade='all, delete-orphan')

    # One-to-many: User can have multiple orders over time
    orders = db.relationship(
        'Order', back_populates='user', cascade='all, delete-orphan')

    # One-to-many: User can write multiple product reviews
    reviews = db.relationship(
        'Review', back_populates='user', cascade='all, delete-orphan')

    # One-to-many: User gets personalized product recommendations
    recommendations = db.relationship(
        'Recommendation', back_populates='user', cascade='all, delete-orphan')
    # One-to-many: User can have multiple sessions
    sessions = db.relationship(
        'UserSession', back_populates='user', cascade='all, delete-orphan')


class CustomerProfile(db.Model):
    """
    Customer Profile Model

    Extended customer information linked to User account.
    One-to-one relationship with User for customer-specific data.

    Attributes:
        user_id (int): Primary key and foreign key to User
        first_name (str): Customer's first name (required)
        last_name (str): Customer's last name (required)
        phone (str): Optional phone number for contact
        default_address_id (int): Optional reference to preferred address

    Design Notes:
        - Separated from User to allow different user types (admin, staff, etc.)
        - Only customers need detailed profile information
        - Default address helps streamline checkout process
    """
    __tablename__ = 'customer_profiles'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    default_address_id = db.Column(
        db.Integer, db.ForeignKey('addresses.id', ondelete='SET NULL'))

    # Relationships
    user = db.relationship('User', back_populates='customer_profile')
    # Self-referential relationship to address, with post_update to avoid circular dependency
    default_address = db.relationship(
        'Address', foreign_keys=[default_address_id], post_update=True)


class Address(db.Model):
    """
    Address Model

    Stores shipping and billing addresses for users.
    Users can have multiple addresses for different purposes.

    Attributes:
        id (int): Primary key, unique address identifier
        user_id (int): Foreign key linking to User who owns this address
        line1 (str): Primary address line (street number, name)
        line2 (str): Optional secondary address line (apt, suite, etc.)
        city (str): City name (required)
        state (str): State/province (required)
        zip_code (str): Postal/ZIP code (required)

    Usage Notes:
        - line1, city, state, zip_code are required for valid addresses
        - line2 is optional for apartment numbers, suite numbers, etc.
        - Can be referenced as default address in CustomerProfile
    """
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    line1 = db.Column(db.String(255), nullable=False)
    line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='addresses')
