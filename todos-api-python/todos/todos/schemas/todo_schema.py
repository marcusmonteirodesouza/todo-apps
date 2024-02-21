from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from todos import db
from todos.todos.models import Todo


class _TodoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        include_relationships = True
        load_instance = True
        sqla_session = db.session


todo_schema = _TodoSchema()
