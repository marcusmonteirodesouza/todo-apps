from marshmallow import Schema, fields


class _CreateToDoTaskRequestSchema(Schema):
    title = fields.String(required=True)
    description = fields.String()


create_todo_task_request_schema = _CreateToDoTaskRequestSchema()
