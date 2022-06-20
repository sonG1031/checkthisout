from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # "환경 변수 APP_CONFIG_FILE에 정의된 파일을 환경 파일로 사용하겠다"는 의미
    app.config.from_envvar('APP_CONFIG_FILE')
    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    api = Api(app)

    #namespace
    from .route.auth import auth
    from .route.img import img
    api.add_namespace(auth, '/auth')
    api.add_namespace(img, '/image')

    return app