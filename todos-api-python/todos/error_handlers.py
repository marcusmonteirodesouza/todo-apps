import dataclasses
import traceback
from dataclasses import dataclass
from enum import StrEnum
from http import HTTPStatus

from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from todos.exceptions import (
    AlreadyExistsException,
    ForbiddenException,
    UnauthorizedException,
    NotFoundException,
)


class _ErrorResponseCode(StrEnum):
    ALREADY_EXISTS = "already_exists"
    BAD_REQUEST = "bad_request"
    FORBIDDEN = "forbidden"
    GENERAL_ERROR = "general_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    UNPROCESSABLE_ENTITY = "unprocessable_entity"


@dataclass
class _ErrorResponse:
    code: _ErrorResponseCode
    message: str


def add_error_handlers(app: Flask, jwt: JWTManager):
    @app.errorhandler(AlreadyExistsException)
    def handle_value_error(e: AlreadyExistsException):
        app.logger.error(e)
        app.logger.error(traceback.format_exc())

        return (
            dataclasses.asdict(
                _ErrorResponse(code=_ErrorResponseCode.ALREADY_EXISTS, message=str(e))
            ),
            HTTPStatus.CONFLICT,
        )

    @app.errorhandler(ForbiddenException)
    def handle_value_error(e: ForbiddenException):
        app.logger.error(e)
        app.logger.error(traceback.format_exc())

        return (
            dataclasses.asdict(
                _ErrorResponse(code=_ErrorResponseCode.FORBIDDEN, message="Forbidden")
            ),
            HTTPStatus.FORBIDDEN,
        )

    @app.errorhandler(UnauthorizedException)
    def handle_value_error(e: UnauthorizedException):
        app.logger.error(e)
        app.logger.error(traceback.format_exc())

        return (
            dataclasses.asdict(
                _ErrorResponse(
                    code=_ErrorResponseCode.UNAUTHORIZED, message="Unauthorized"
                )
            ),
            HTTPStatus.UNAUTHORIZED,
        )

    @app.errorhandler(NotFoundException)
    def handle_value_error(e: NotFoundException):
        app.logger.error(e)
        app.logger.error(traceback.format_exc())

        return (
            dataclasses.asdict(
                _ErrorResponse(code=_ErrorResponseCode.NOT_FOUND, message=str(e))
            ),
            HTTPStatus.NOT_FOUND,
        )

    @app.errorhandler(ValueError)
    def handle_value_error(e: ValueError):
        app.logger.error(e)
        app.logger.error(traceback.format_exc())

        return (
            dataclasses.asdict(
                _ErrorResponse(
                    code=_ErrorResponseCode.UNPROCESSABLE_ENTITY, message=str(e)
                )
            ),
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        try:
            app.logger.error(e.validation_error.json())
        except AttributeError:
            app.logger.error(e)

        app.logger.error(traceback.format_exc())

        code = (
            _ErrorResponseCode.BAD_REQUEST
            if e.code == HTTPStatus.BAD_REQUEST
            else _ErrorResponseCode.GENERAL_ERROR
        )

        return (
            dataclasses.asdict(_ErrorResponse(code=code, message=e.description)),
            e.code,
        )

    @app.errorhandler(Exception)
    def handle_exception(e: Exception):
        app.logger.error(f"{e.__class__.__name__}: {e}")
        app.logger.error(traceback.format_stack())

        return (
            dataclasses.asdict(
                _ErrorResponse(
                    code=_ErrorResponseCode.GENERAL_ERROR,
                    message="Internal Server Error",
                )
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            dataclasses.asdict(
                _ErrorResponse(
                    code=_ErrorResponseCode.UNAUTHORIZED, message="Token has expired"
                )
            ),
            HTTPStatus.UNAUTHORIZED,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(reason: str):
        return (
            dataclasses.asdict(
                _ErrorResponse(code=_ErrorResponseCode.UNAUTHORIZED, message=reason)
            ),
            HTTPStatus.UNAUTHORIZED,
        )

    @jwt.unauthorized_loader
    def unauthorized_callback(reason: str):
        return (
            dataclasses.asdict(
                _ErrorResponse(code=_ErrorResponseCode.UNAUTHORIZED, message=reason)
            ),
            HTTPStatus.UNAUTHORIZED,
        )
