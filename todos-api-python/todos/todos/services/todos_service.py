from typing import Optional
from todos import db
from todos.exceptions import NotFoundException
from todos.todos.models import Todo, TodoTask


class TodosService:
    def __init__(self) -> None:
        pass

    def create_todo(self, owner_id: str, title: str) -> Todo:
        todo = Todo(owner_id=owner_id, title=title)

        db.session.add(todo)

        db.session.commit()

        return todo

    def get_todo(self, id: str) -> Optional[Todo]:
        return Todo.query.filter_by(id=id).one_or_none()

    def create_todo_task(
        self, todo_id: str, title: str, description: Optional[str] = None
    ) -> TodoTask:
        todo = self.get_todo(id=todo_id)

        if not todo:
            raise NotFoundException(f"ToDo {todo_id} not found")

        todo_task = TodoTask(todo=todo, title=title, description=description)

        db.session.add(todo_task)

        db.session.commit()

        return todo_task

    def get_todo_task(self, id: str) -> Optional[TodoTask]:
        return TodoTask.query.filter_by(id=id).one_or_none()

    def update_todo_task(self, id: str, is_completed: Optional[bool]) -> TodoTask:
        todo_task = TodoTask.query.filter_by(id=id).one_or_none()

        if not todo_task:
            raise NotFoundException("ToDo task {id} not found")

        if is_completed:
            todo_task.is_completed = is_completed

        db.session.commit()

        return todo_task
