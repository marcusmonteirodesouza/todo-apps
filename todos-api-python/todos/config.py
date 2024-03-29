import os


class _Config:
    DEBUG = True if os.environ.get("DEBUG") else False
    GOOGLE_OAUTH_CLIENT_ID = os.environ["GOOGLE_OAUTH_CLIENT_ID"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    LOG_LEVEL = os.environ["LOG_LEVEL"]
    PORT = int(os.environ["PORT"])
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"

    @staticmethod
    def init_app(app):
        pass


config = _Config()
