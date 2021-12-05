import logging

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from waitress import serve

import settings
from database.db import db, uri_db
from views.views import VistaSignUp, VistaTasks, VistaTask, \
    VistaLogIn, VistaFiles, VistaHealth


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri_db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS']=True
    return app


logging.basicConfig(format=settings.LOG_PATTERN, level=logging.INFO)

app = create_app()
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(VistaHealth, '/health')
api.add_resource(VistaSignUp, '/auth/signup')
api.add_resource(VistaLogIn, '/auth/login')
api.add_resource(VistaTasks, '/tasks/<int:id_user>')
api.add_resource(VistaTask, '/task/<int:id_task>')
api.add_resource(VistaFiles, '/files/<int:id_user>/<filename>/<int:status>')

jwt=JWTManager(app)


if __name__ == "__main__":
    logging.info('Server started')
    serve(
        app=app,
        host='0.0.0.0',
        port=8080,
        threads=settings.WAITRESS_WORKERS,
        connection_limit=settings.WAITRESS_CHANNELS,
    )
