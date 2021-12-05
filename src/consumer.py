import os
import json
from datetime import datetime

from subprocess import Popen, PIPE
import psycopg2

import settings
from utils.s3_utils import s3_download_file, s3_upload_file
from utils.sqs_utils import sqs, delete_messages, receive_messages



def unpack_message(msg):
    try:
        return (
            msg.message_attributes.get("path", {}).get("StringValue",
                                                       "unknown"),
            msg.message_attributes.get("file_name", {}).get("StringValue",
                                                            "unknown"),
            msg.message_attributes.get("old_format", {}).get("StringValue",
                                                             "unknown"),
            msg.message_attributes.get("id", {}).get("StringValue",
                                                     "unknown"),
        )
    except:
        return "", msg.body, 0


def pull_tasks():
    """
    Pull messages from sqs and invoke celery task.
    :return:
    """
    print(f"[{datetime.now()}] Listening for messages...")
    queue = sqs.get_queue_by_name(QueueName="conversiones")
    received_messages = receive_messages(queue=queue, max_number=10,wait_time=2)        
    if received_messages:
        for msg in received_messages:
            body = msg.body
            body = body.replace("'","\"")
            varJson = json.loads(body)
            change_format_audio(varJson["path"], varJson["file_name"], varJson["old_format"], varJson["id"])
            print(f'[{datetime.now()}] Body: {msg.body}')     
   
        delete_messages(queue, received_messages)


def change_format_audio(path, file_name, old_format, id):
    id = int(id)
    rest = obtenerValoresDeTarea(id)
    email = rest[0][0]    
    formato = rest[0][1]
    local_path = s3_download_file(s3_path=path, file_name=file_name)
    new_local_path = local_path.replace(old_format, "."+formato)
    new_file_name = file_name.replace(old_format, "."+formato)

    convertir_audio(local_path, new_local_path)
    new_s3_path = s3_upload_file(local_path=new_local_path, file_name=new_file_name)
    actualizarTarea(new_s3_path, id)
    os.remove(local_path)
    os.remove(new_local_path)

def obtenerValoresDeTarea(id):
    conn = psycopg2.connect(host=settings.PG_HOST, port=settings.PG_PORT, database=settings.PG_DATABASE, user=settings.PG_USER, password=settings.PG_PASSWORD)
    cur = conn.cursor()
    query = 'select u.email, task.new_format from task inner join public."user" u on task.user = u.id where task.id = ' + str(id) + ';'
    cur.execute(query)
    rest = [fila for fila in cur]
    cur.close()
    conn.close()
    return rest

def actualizarTarea(new_path, id):
    conn = psycopg2.connect(host=settings.PG_HOST, port=settings.PG_PORT, database=settings.PG_DATABASE, user=settings.PG_USER, password=settings.PG_PASSWORD)
    cur = conn.cursor()
    query = 'update task set new_path = \'' + new_path + '\', status = \'processed\' where id = ' + str(id) + ';'   
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def convertir_audio( path, new_path ):
    p = Popen(['ffmpeg', '-i', path, new_path], stdin=PIPE, stdout=PIPE)
    p.stdin.write(b"y\n")
    p.communicate()
    p.stdin.close()


if __name__ == '__main__':
    while True:
        pull_tasks()
