import os

APP = 'Cloud-Group-8'
APP_VERSION = "1.0.0"
LOG_PATTERN = '%(asctime)s.%(msecs)s:%(name)s:%(thread)d:(%(threadName)-10s):%(levelname)s:%(process)d:%(message)s'

# POSTGRESQL
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
PG_HOST = os.getenv('PG_HOST', '')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DATABASE = os.getenv('PG_DATABASE', 'bdconversion')

# S3
BUCKET = os.getenv("BUCKET", "bucket-grupo8-nube")
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', "")
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', "")
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN', "")

# WAITRESS CONFIG
WAITRESS_WORKERS = int(os.getenv('WAITRESS_WORKERS', 8))
WAITRESS_CHANNELS = int(os.getenv('WAITRESS_CHANNELS', 100))
