import os
class Config:
    SECRET_KEY = os.environ.get('SECRET KEY')  or 'default-secret-key'

    SQLALCHEMY_DATABASE_URI = r'sqlite:///C:\Users\vicky\db\anpr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False