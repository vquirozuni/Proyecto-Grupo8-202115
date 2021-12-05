import os

APP = 'Cloud-Group-8'
APP_VERSION = "1.0.0"
LOG_PATTERN = '%(asctime)s.%(msecs)s:%(name)s:%(thread)d:(%(threadName)-10s):%(levelname)s:%(process)d:%(message)s'

# POSTGRESQL
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
PG_HOST = os.getenv('PG_HOST', 'miso-grupo8.cqeaj94zhds3.us-east-1.rds.amazonaws.com')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DATABASE = os.getenv('PG_DATABASE', 'bdconversion')

# S3
BUCKET = os.getenv("BUCKET", "bucket-grupo8-nube")
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', "ASIAQPOUW3HC4VNDFNQ2")
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', "RCEUN7637iZSPov2+UyJw5CJRfTvZ4uXKQwsa4j0")
AWS_SESSION_TOKEN = os.getenv('AWS_SESSION_TOKEN', "FwoGZXIvYXdzELT//////////wEaDCNGVIdlGbBDvQjVtiLJAQZem82yAkmtpzHJFlPjrjVmytALo/T2H6L0vZnjewA/VHrJ4uUUItoyJkrZ+bZHyq+0DMq3Go3wNr+FmkORvCoVI8H6KZ69BzAgL4Try6JPQp8moSi0kW4GLhnh1K71jGC+KWvdFK2WsQioVmzFx4N4gCVsIjTBAHGv8nRgaDApGlEV/cfucCbugwJdSqMVScSHMSGw+wUhaOqJ8+BgRCATZOr8qHoRgnbXZqaoC8rRpn3QzacsLCFGTGcKlFgS048pjBxUTzT3ryjgi7SNBjIt2VKoxHcRySLBiiKgjYDXkc++aoDSoIwqx6XWTGowpqd54aRbdXPtx8to+9ce")

# WAITRESS CONFIG
WAITRESS_WORKERS = int(os.getenv('WAITRESS_WORKERS', 8))
WAITRESS_CHANNELS = int(os.getenv('WAITRESS_CHANNELS', 100))
