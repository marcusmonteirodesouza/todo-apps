import io
import mimetypes
import pathlib
import os.path
import uuid
from http import HTTPStatus
from flask import Blueprint, current_app, request

from todos.exceptions import NotFoundException
from todos.todos.schemas import todo_schema

todos_blueprint = Blueprint("todos", __name__, url_prefix="/todos")


@todos_blueprint.post("/")
def create_todo():
    todo = current_app.todos_service.create_todo()

    return todo_schema.dump(todo), HTTPStatus.CREATED


@todos_blueprint.get("/<id>")
def get_todo(id: str):
    todo = current_app.todos_service.get_todo(id=id)

    if not todo:
        raise NotFoundException(f"Todo {id} not found")

    return todo_schema.dump(todo)
