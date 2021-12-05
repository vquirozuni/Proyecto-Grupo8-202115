from flask_sqlalchemy import SQLAlchemy

import settings

db = SQLAlchemy()
uri_db = "postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/" \
         "{PG_DATABASE}".format(
    PG_USER=settings.PG_USER,
    PG_PASSWORD=settings.PG_PASSWORD,
    PG_HOST=settings.PG_HOST,
    PG_PORT=settings.PG_PORT,
    PG_DATABASE=settings.PG_DATABASE
)