from datetime import datetime
from extensions import db


class UserSession(db.Model):
    """
    User Session Model

    Tracks user login sessions for analytics and security monitoring.
    Records login timestamps, IP addresses, and session durations.

    Attributes:
        id (int): Primary key, unique session identifier
        user_id (int): Foreign key to User who owns this session
        ip_address (str): IP address of the user during the session
        user_agent (str): User agent string from the client's request
        created_at (datetime): Timestamp when the session was created
        updated_at (datetime): Timestamp when the session was last updated
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

    @property
    def session_duration(self):
        """Calculate duration of the session in seconds"""
        if self.session_end and self.session_start:
            return int((self.updated_at - self.created_at).total_seconds())

    # Relationships
    user = db.relationship('User', back_populates='sessions')
