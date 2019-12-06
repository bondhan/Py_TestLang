from flask_marshmallow import Schema
from marshmallow import post_load
from flask_marshmallow.fields import fields

class PaymentIsoClientData(object):
    def __init__(self, organisation_id, trx_type_id, trx_amount, va_number, location, transaction_date, description,
                 trace_number, username, customer_name, obu_wallet_id, customer_id):
        self.organisation_id = organisation_id
        self.trx_type_id = trx_type_id
        self.trx_amount = trx_amount
        self.va_number = va_number
        self.location = location
        self.transaction_date = transaction_date
        self.description = description
        self.trace_number = trace_number
        self.username = username
        self.customer_name = customer_name
        self.obu_wallet_id = obu_wallet_id
        self.customer_id = customer_id


class PaymentIsoClientRequestSchema(Schema):
    class Meta:
        strict = True
        required = True
        allow_none = False

    organisation_id = fields.Integer()
    trx_type_id = fields.Integer()
    trx_amount = fields.Number()
    va_number = fields.Str()
    location = fields.Str()
    transaction_date = fields.DateTime()
    description = fields.Str()
    trace_number = fields.Str()
    username = fields.Str()
    customer_name = fields.Str()
    obu_wallet_id = fields.Integer()
    customer_id = fields.Integer()

    @post_load
    def get_payment_isoclient_request(self, data):
        return PaymentIsoClientData(**data)
