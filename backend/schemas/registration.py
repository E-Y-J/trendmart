from marshmallow import fields
from extensions import BaseSchema
from models.registration import User, CustomerProfile, Address

# -------Read and Write Schemas------- #


class AddressSchema(BaseSchema):
    class Meta:
        model = Address
