from http import HTTPStatus
from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from todos.exceptions import ForbiddenException, NotFoundException
from todos.todos.schemas import todo_schema, todo_task_schema

todos_blueprint = Blueprint("todos", __name__, url_prefix="/todos")


@todos_blueprint.post("/")
@jwt_required()
def create_todo():
    current_user = get_jwt_identity()

    todo = current_app.todos_service.create_todo(owner_id=current_user)

    return todo_schema.dump(todo), HTTPStatus.CREATED


@todos_blueprint.post("/<todo_id>/tasks")
@jwt_required()
def create_todo_task(todo_id: str):
    todo = current_app.todos_service.get_todo(id=todo_id)

    if not todo:
        raise NotFoundException(f"Todo {todo_id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    todo_task = current_app.todos_service.create_todo_task(
        todo_id=todo.id, title=request.json["title"]
    )

    return todo_task_schema.dump(todo_task), HTTPStatus.CREATED


@todos_blueprint.get("/<id>")
@jwt_required()
def get_todo(id: str):
    todo = current_app.todos_service.get_todo(id=id)

    if not todo:
        raise NotFoundException(f"Todo {id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    return todo_schema.dump(todo)


@todos_blueprint.get("/<todo_id>/tasks/<todo_task_id>")
@jwt_required()
def get_todo_task(todo_id: str, todo_task_id: str):
    todo = current_app.todos_service.get_todo(id=todo_id)

    if not todo:
        raise NotFoundException(f"Todo {todo_id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    todo_task = current_app.todos_service.get_todo_task(id=todo_task_id)

    if not todo_task:
        raise NotFoundException(f"Todo Task {todo_task_id} not found")

    return todo_task_schema.dump(todo_task)
