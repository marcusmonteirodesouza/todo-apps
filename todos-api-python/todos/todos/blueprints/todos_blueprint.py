from http import HTTPStatus
from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from todos.exceptions import ForbiddenException, NotFoundException
from todos.todos.schemas import (
    create_todo_request_schema,
    create_todo_task_request_schema,
    todo_schema,
    todo_task_schema,
)

todos_blueprint = Blueprint("todos", __name__, url_prefix="/todos")


@todos_blueprint.post("/")
@jwt_required()
def create_todo():
    try:
        create_todo_request = create_todo_request_schema.load(request.json)
    except ValidationError as e:
        raise ValueError(str(e))

    current_user = get_jwt_identity()

    todo = current_app.todos_service.create_todo(
        owner_id=current_user, title=create_todo_request["title"]
    )

    return todo_schema.dump(todo), HTTPStatus.CREATED


@todos_blueprint.post("/<todo_id>/tasks")
@jwt_required()
def create_todo_task(todo_id: str):
    try:
        create_todo_task_request = create_todo_task_request_schema.load(request.json)
    except ValidationError as e:
        raise ValueError(str(e))

    todo = current_app.todos_service.get_todo(id=todo_id)

    if not todo:
        raise NotFoundException(f"ToDo {todo_id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    todo_task = current_app.todos_service.create_todo_task(
        todo_id=todo.id,
        title=create_todo_task_request["title"],
        description=create_todo_task_request["description"],
    )

    return todo_task_schema.dump(todo_task), HTTPStatus.CREATED


@todos_blueprint.get("/<id>")
@jwt_required()
def get_todo(id: str):
    todo = current_app.todos_service.get_todo(id=id)

    if not todo:
        raise NotFoundException(f"ToDo {id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    return todo_schema.dump(todo)


@todos_blueprint.patch("/<id>/complete")
@jwt_required()
def complete_todo(id: str):
    todo = current_app.todos_service.get_todo(id=id)

    if not todo:
        raise NotFoundException(f"ToDo {id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    updated_todo = current_app.todos_service.update_todo(id=todo.id, is_completed=True)

    return todo_schema.dump(updated_todo)


@todos_blueprint.patch("/<id>/uncomplete")
@jwt_required()
def uncomplete_todo(id: str):
    todo = current_app.todos_service.get_todo(id=id)

    if not todo:
        raise NotFoundException(f"ToDo {id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    updated_todo = current_app.todos_service.update_todo(id=todo.id, is_completed=False)

    return todo_schema.dump(updated_todo)


@todos_blueprint.patch("/<todo_id>/tasks/<todo_task_id>/complete")
@jwt_required()
def complete_todo_task(todo_id: str, todo_task_id: str):
    todo = current_app.todos_service.get_todo(id=todo_id)

    if not todo:
        raise NotFoundException(f"ToDo {todo_id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    todo_task = current_app.todos_service.get_todo_task(id=todo_task_id)

    if not todo_task:
        raise NotFoundException(f"ToDo task {todo_task_id} not found")

    if todo_task.todo_id != todo.id:
        raise ValueError("Task {todo_task.id} does not belong to ToDo {todo.id}")

    updated_todo_task = current_app.todos_service.update_todo_task(
        id=todo_task.id, is_completed=True
    )

    return todo_task_schema.dump(updated_todo_task)


@todos_blueprint.patch("/<todo_id>/tasks/<todo_task_id>/uncomplete")
@jwt_required()
def uncomplete_todo_task(todo_id: str, todo_task_id: str):
    todo = current_app.todos_service.get_todo(id=todo_id)

    if not todo:
        raise NotFoundException(f"ToDo {todo_id} not found")

    current_user = get_jwt_identity()

    if current_user != todo.owner_id:
        raise ForbiddenException(
            f"User {current_user} is not the owner of ToDo {todo.id}"
        )

    todo_task = current_app.todos_service.get_todo_task(id=todo_task_id)

    if not todo_task:
        raise NotFoundException(f"ToDo task {todo_task_id} not found")

    if todo_task.todo_id != todo.id:
        raise ValueError("Task {todo_task.id} does not belong to ToDo {todo.id}")

    updated_todo_task = current_app.todos_service.update_todo_task(
        id=todo_task.id, is_completed=False
    )

    return todo_task_schema.dump(updated_todo_task)
