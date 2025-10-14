from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Interger, primary_key=True)
    email = db.Column(db.String(125), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='customer')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CustomerProfile(db.Model):
    __tablename__ = 'customer_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    default_address_id = db.Column(
        db.Integer, db.ForeignKey('addresses.id', ondelete='SET NULL'))


class Address(db.Model):
    __tablename__ = 'adresses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Interger, db.ForeignKey('users.id'), nullable=False)
    line1 = db.Column(db.String(255), nullable=False)
    line2 = db.Column(db.String(255))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    user = db.relationship('User', backref=db.backref(
        'customer_profile', userlist=False))
