from typing import Optional
from todos import db
from todos.todos.models import Todo


class TodosService:
    def __init__(self) -> None:
        pass

    def create_todo(self) -> Todo:
        todo = Todo()

        db.session.add(todo)

        db.session.commit()

        return todo

    def get_todo(self, id: str) -> Optional[Todo]:
        return Todo.query.filter_by(id=id).one_or_none()
