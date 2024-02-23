from marshmallow import Schema, fields


class _CreateToDoRequestSchema(Schema):
    title = fields.String(required=True)


create_todo_request_schema = _CreateToDoRequestSchema()
