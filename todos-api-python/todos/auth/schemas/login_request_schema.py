from marshmallow import Schema, fields


class _LoginRequestSchema(Schema):
    token = fields.String(required=True)


login_request_schema = _LoginRequestSchema()
