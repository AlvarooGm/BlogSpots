from flask_sqlalchemy import SQLAlchemy


class Config:
    DEBUG = True
    SECRET_KEY='dev'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:admin@localhost:5432/postsBd"
    CKEDITOR_PKG_TYPE = 'basic'
    