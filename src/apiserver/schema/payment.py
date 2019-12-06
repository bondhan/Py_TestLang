import logging

from flask_marshmallow import Schema
from marshmallow import post_load, validate
from flask_marshmallow.fields import fields
from config.flask_config_apiserver import ma_apiserver


logger = logging.getLogger(__name__)

class PaymentClass(object):
    def __init__(self, customer_id, wallet_id, customer_name, username, balance):
        self.customer_id = customer_id
        self.wallet_id = wallet_id
        self.customer_name = customer_name
        self.username = username
        self.balance = balance


class PaymentSchema(ma_apiserver.ModelSchema):
    class Meta:
        strict = True
        required = True
        allow_none = False

    customer_id = fields.Int()
    wallet_id = fields.Int()
    customer_name = fields.Str()
    username = fields.Str()
    balance = fields.Number()

    @post_load
    def get_payment(self, data):
        return PaymentClass(**data)


class PaymentData(object):
    def __init__(self, obu_serial_number, trx_type_id, trx_amount, location, transaction_date, description,
                 trace_number):
        self.obu_serial_number = obu_serial_number
        self.trx_type_id = trx_type_id
        self.trx_amount = trx_amount
        self.location = location
        self.transaction_date = transaction_date
        self.description = description
        self.trace_number = trace_number


class PaymentRequestSchema(Schema):
    class Meta:
        strict = True
        required = True
        allow_none = False

    obu_serial_number = fields.Str(validate=[validate.Length(min=10, max=50)])
    trx_type_id = fields.Str(validate=[validate.Length(min=1)])
    trx_amount = fields.Str(validate=[validate.Length(min=1, max=16)])
    location = fields.Str(validate=[validate.Length(min=1, max=45)])
    transaction_date = fields.Str(validate=[validate.Length(min=1)])
    description = fields.Str(validate=[validate.Length(min=1)])
    trace_number = fields.Str(validate=[validate.Length(min=1)])

    @post_load
    def get_payment_request(self, data):
        return PaymentData(**data)
