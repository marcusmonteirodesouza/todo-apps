from http import HTTPStatus
from flask import Blueprint, current_app, request

from todos.exceptions import NotFoundException
from todos.todos.schemas import todo_schema, todo_task_schema

todos_blueprint = Blueprint("todos", __name__, url_prefix="/todos")


@todos_blueprint.post("/")
def create_todo():
    todo = current_app.todos_service.create_todo()

    return todo_schema.dump(todo), HTTPStatus.CREATED


@todos_blueprint.post("/<todo_id>/tasks")
def create_todo_task(todo_id: str):
    todo_task = current_app.todos_service.create_todo_task(
        todo_id=todo_id, title=request.json["title"]
    )

    return todo_task_schema.dump(todo_task), HTTPStatus.CREATED


@todos_blueprint.get("/<id>")
def get_todo(id: str):
    todo = current_app.todos_service.get_todo(id=id)

    if not todo:
        raise NotFoundException(f"Todo {id} not found")

    return todo_schema.dump(todo)


@todos_blueprint.get("/<todo_id>/tasks/<todo_task_id>")
def get_todo_task(todo_id: str, todo_task_id: str):
    todo_task = current_app.todos_service.get_todo_task(id=todo_task_id)

    if not todo_task:
        raise NotFoundException(f"Todo Task {todo_task_id} not found")

    return todo_task_schema.dump(todo_task)
