from datetime import datetime
from extensions import db


class UserSession(db.Model):
    """
    User Session Model for Behavioral Analytics (Must-Have)

    Tracks comprehensive user session data for analytics and security monitoring.
    Essential for understanding user engagement patterns and behavior.

    Attributes:
        id (int): Primary key, unique session identifier
        user_id (int): Foreign key to User who owns this session
        ip_address (str): IP address of the user during the session (45 chars for IPv6)
        user_agent (str): User agent string from the client's request
        session_start (datetime): Timestamp when the session began
        session_end (datetime): Timestamp when the session ended (nullable for active sessions)
        pages_visited (int): Count of pages viewed during this session
        updated_at (datetime): Timestamp when the session was last updated

        # Computed Properties
        session_duration (property): Calculated duration in seconds

    Analytics Features:
        - Track user engagement duration and patterns
        - Monitor session activity and page navigation
        - Support both authenticated and guest session tracking
        - Enable security analysis through IP and user agent tracking

    Business Value:
        - Understand user behavior and engagement
        - Identify popular navigation patterns
        - Optimize user experience based on session data
        - Support security monitoring and fraud detection
    """
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    session_start = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)
    session_end = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(),
                           onupdate=db.func.now(), nullable=False)
    pages_visited = db.Column(db.Integer, default=0, nullable=False)
    click_path = db.Column(db.text)  # JSON string of page navigation path
    time_per_page = db.Column(db.Float)

    @property
    def session_duration(self):
        """Calculate duration of the session in seconds"""
        if self.session_end:
            return (self.session_end - self.session_start).total_seconds()
        return (datetime.utcnow() - self.session_start).total_seconds()

    # Relationships
    user = db.relationship('User', back_populates='sessions')


class ProductView(db.Model):
    """
    Product View Tracking Model for Behavioral Analytics (Must-Have)

    Tracks individual product page views for comprehensive behavioral analytics.
    Essential for understanding product interest, engagement, and conversion patterns.

    Attributes:
        id (int): Primary key, unique view identifier
        product_id (int): Foreign key to Product being viewed
        user_id (int): Foreign key to User who viewed the product (nullable for guest views)
        session_id (str): Foreign key to UserSession during which the product was viewed
        view_time (int): Time spent viewing the product in seconds
        viewed_at (datetime): Timestamp when the product view occurred
        added_to_cart (bool): Flag indicating if the product was added to cart during this view

    Analytics Features:
        - Track product engagement and interest levels
        - Measure time spent on product pages
        - Monitor conversion from view to cart addition
        - Support both authenticated and guest user tracking
        - Link views to specific user sessions for journey analysis

    Business Value:
        - Identify most engaging products and optimize catalog
        - Understand customer interest patterns and preferences
        - Measure product page effectiveness and conversion rates
        - Provide data for recommendation algorithm improvement
        - Support A/B testing of product page designs
    """
    __tablename__ = 'product_views'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    session_id = db.Column(db.String(255), db.ForeignKey(
        'user_sessions.id'), nullable=True)
    # seconds spent viewing
    view_time = db.Column(db.Integer, default=0, nullable=False)
    viewed_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    added_to_cart = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    product = db.relationship('Product', back_populates='views')
    user = db.relationship('User', back_populates='product_views')
