from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from todos import db
from todos.todos.models import Todo
from todos.todos.schemas.todo_task_schema import _TodoTaskSchema


class _TodoSchema(SQLAlchemyAutoSchema):
    tasks = fields.Nested(_TodoTaskSchema, many=True)

    class Meta:
        model = Todo
        include_relationships = True
        load_instance = True
        sqla_session = db.session


todo_schema = _TodoSchema()
