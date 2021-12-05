import os
import logging
from datetime import datetime

import werkzeug
from flask import request, send_file
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, create_access_token

from database.models import User, Task
from database.db import db
from schemas.schemas import TaskSchema, UserSchema
from utils.s3_utils import s3_upload_file, s3_download_file
from utils.sqs_utils import sqs, send_message, build_pack

import settings


usuario_schema = UserSchema()
task_schema = TaskSchema()


class VistaHealth(Resource):
    def get(self):
        return {"status":"ok"}, 200

class VistaLogIn(Resource):
    def post(self):
        logging.info(f'{settings.APP}: Vista login: post')
        u_username = request.json["username"]
        userName = User.query.filter_by(user_name=u_username).all()
        if not userName:
            logging.info(f'{settings.APP}: Login: user unknown')
            return {"mensaje": "username o password equivocado"}

        u_password = request.json["password"]
        user = User.query.filter_by(user_name=u_username, password=u_password).all()
        if not user:
            logging.info(f'{settings.APP}: Login: invalid password')
            return {"mensaje": "username o password equivocado"}

        token = create_access_token(identity=u_username)
        logging.info(f'{settings.APP}: Vista login: done')
        return {"token":token}


class VistaSignUp(Resource):

    def post(self):
        logging.info(f'{settings.APP}: Vista Sign up: post')
        u_username = request.json["username"]
        userName = User.query.filter_by(user_name=u_username).all()
        if userName:
            logging.info(f'{settings.APP}: Vista Sign up: invalid user')
            return {"mensaje": "username ya existe"}

        u_email = request.json["email"]
        userEmail = User.query.filter_by(email=u_email).all()
        if userEmail:
            logging.info(f'{settings.APP}: Vista Sign up: invalid email')
            return {"mensaje": "Email ya existe"}

        u_password1 = request.json["password1"]
        u_password2 = request.json["password2"]
        if u_password1 != u_password2:
            logging.info(f'{settings.APP}: Vista Sign up: invalid password')
            return {"mensaje": "Password no coinciden"}

        new_user = User(user_name = u_username, password = u_password1, email = u_email)
        db.session.add(new_user)
        db.session.commit()
        logging.info(f'{settings.APP}: Vista Sign up: new user {new_user.id}')
        return {"mensaje": "Cuenta se creó satisfactoriamente", "user_id":new_user.id}


class VistaTasks(Resource):
    @jwt_required()
    def post(self, id_user):
        logging.info(f'{settings.APP}: Vista Tasks: post')
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('fileName', type=werkzeug.datastructures.FileStorage, location='files')
        self.parser.add_argument('newFormat')
        args = self.parser.parse_args()
        audio_file = args.get("fileName")
        path = f'./{audio_file.filename}'
        audio_file.save(path)
        s3_path = s3_upload_file(local_path=path,
                                 file_name=audio_file.filename)
        logging.info(f'{settings.APP}: Vista Tasks: save file in {s3_path}')

        task = Task(file_path=s3_path, new_format=args.get("newFormat"),
                    status='uploaded', time_stamp=datetime.utcnow(),
                    user=id_user, new_path='')
        db.session.add(task)
        db.session.commit()

        arg = dict(
            path=s3_path,
            file_name=audio_file.filename,
            old_format=os.path.splitext(path)[1],
            id = str(task.id)
        )
        pack = build_pack(**arg)
        queue = sqs.get_queue_by_name(QueueName="conversiones")
        send_message(queue=queue,
                     message_body=f"{arg}",
                     message_attributes=pack
                     )
        logging.info(f'{settings.APP}: Vista Tasks: jump  queue id task {task.id}')
        os.remove(path)


        return {"mensaje":"Tarea fue creada"}, 200
        
    @jwt_required()
    def get(self, id_user):
        logging.info(f'{settings.APP}: Vista Tasks: get')
        user = User.query.get_or_404(id_user)
        return [task_schema.dump(u) for u in user.tasks]
        


class VistaTask(Resource):
    @jwt_required()
    def get(self, id_task):
        return task_schema.dump(Task.query.get_or_404(id_task))

    @jwt_required()
    def put(self, id_task: int):
        task = Task.query.get_or_404(id_task)
        if not task:
            return {"mensaje": "Tarea no disponible"}
        
        if task.status == 'uploaded':
            task.new_format = request.json['new_format']
            db.session.commit()
            return {"mensaje":"Se actualizó el nuevo formato de conversión"}
        
        if not delete_s3_file(task.new_path):
            return {"mensaje":"Error al eliminar archivo elegido"}
        #os.remove(task.new_path)
        task.new_format = request.json['new_format']
        task.new_path = ''
        task.status = 'uploaded'
        db.session.commit()

        arg = dict(
            path=task.file_path,
            old_format=os.path.splitext(task.file_path)[1],
            id = id_task
        )
        pack = build_pack(**arg)
        queue = sqs.get_queue_by_name(QueueName="conversiones")
        send_message(queue=queue,
                     message_body=f'reload task {id_task} to the queue',
                     message_attributes=pack
                     )

        return {"mensaje":"Cambio realizado de archivo processed"}

    @jwt_required()
    def delete(self, id_task: int):
        task = Task.query.get_or_404(id_task)
        if not task:
            return {"mensaje":"Tarea no existe"}
        
        if not delete_s3_file(task.file_path):
            return {"mensaje":"Error al eliminar archivo original."}

        if not delete_s3_file(task.new_path):
            return {"mensaje":"Error al eliminar archivo procesado."}
        #os.remove(task.file_path)
        #os.remove(task.new_path)
        db.session.delete(task)
        db.session.commit()
        return {"mensaje":"Se eliminó la tarea"}, 204


class VistaFiles(Resource):
    @jwt_required()
    def get(self, id_user: int, filename: str, status: int):
        task = Task.query.filter_by(user=id_user).all()
        if not task:
           return "Usuario no tiene archivos registrados"
       
        arch_originales = [task_schema.dump(u)['file_path'] for u in task]
        arch_procesados = [task_schema.dump(u)['new_path'] for u in task]
    

        if status == 0:
            audios = [path for path in arch_originales if path.find(filename) > -1]
        else:    
            audios = [path for path in arch_procesados if path.find(filename) > -1]

        if not len(audios) > 0:
            return 'Audio no existe'

        path_audio = audios[0]
        local_path = s3_download_file(s3_path=path_audio, file_name=filename)
        return send_file(local_path, as_attachment = True)
