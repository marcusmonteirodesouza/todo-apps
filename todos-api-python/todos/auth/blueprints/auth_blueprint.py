from flask import Blueprint, current_app, request
from flask_jwt_extended import create_access_token
from google.auth.transport import requests
from google.oauth2 import id_token
from marshmallow import ValidationError

from todos import config
from todos.auth.schemas import login_request_schema
from todos.exceptions import UnauthorizedException

auth_blueprint = Blueprint("auth", __name__, url_prefix="/")


@auth_blueprint.post("/login")
def login():
    try:
        login_request = login_request_schema.load(request.json)
    except ValidationError as e:
        raise ValueError(str(e))

    # Validate Google ID token
    try:
        id_info = id_token.verify_oauth2_token(
            id_token=login_request["token"],
            request=requests.Request(),
            audience=config.GOOGLE_OAUTH_CLIENT_ID,
        )
    except Exception as e:
        current_app.logger.exception(e)
        raise UnauthorizedException(str(e))

    access_token = create_access_token(identity=id_info["sub"])
    return {"access_token": access_token}
