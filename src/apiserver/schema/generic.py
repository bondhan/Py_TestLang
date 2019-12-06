import logging
from flask_marshmallow import Schema
from flask_marshmallow.fields import fields
from marshmallow import post_load, validate

logger = logging.getLogger(__name__)

class Generic(object):
    def __init__(self, organisation_id, data):
        self.organisation_id = organisation_id
        self.data = data


class GenericRequestSchema(Schema):
    class Meta:
        strict = True
        required = True
        allow_none = False

    organisation_id = fields.Str(validate=[validate.Length(min=1)])
    data = fields.Str(validate=[validate.Length(min=1)])

    @post_load
    def get_request(self, data):
        return Generic(**data)
