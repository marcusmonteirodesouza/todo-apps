from typing import Optional
from todos import db
from todos.exceptions import NotFoundException
from todos.todos.models import Todo, TodoTask


class TodosService:
    def __init__(self) -> None:
        pass

    def create_todo(self, owner_id: str) -> Todo:
        todo = Todo(owner_id=owner_id)

        db.session.add(todo)

        db.session.commit()

        return todo

    def get_todo(self, id: str) -> Optional[Todo]:
        return Todo.query.filter_by(id=id).one_or_none()

    def create_todo_task(self, todo_id: str, title: str) -> TodoTask:
        todo = self.get_todo(id=todo_id)

        if not todo:
            raise NotFoundException(f"Todo {todo_id} not found")

        todo_task = TodoTask(todo=todo, title=title)

        db.session.add(todo_task)

        db.session.commit()

        return todo_task

    def get_todo_task(self, id: str) -> Optional[TodoTask]:
        return TodoTask.query.filter_by(id=id).one_or_none()
