from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields

from todos import db
from todos.todos.models import TodoTask
from todos.todos.schemas import todo_schema


class _TodoTaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TodoTask
        include_relationships = True
        load_instance = True
        sqla_session = db.session

    batch = fields.Nested(todo_schema)


todo_task_schema = _TodoTaskSchema()
