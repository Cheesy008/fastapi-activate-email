import os
from dotenv import load_dotenv

load_dotenv('.env')

EXPIRE_TIME = 6 * 3600

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
ALLOW_ORIGINS = os.environ.get('ALLOW_ORIGINS').split(',')

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

HOST = os.environ.get('MAIL_HOST')
PORT = os.environ.get('MAIL_PORT')
SENDER_EMAIL = os.environ.get('SENDER_MAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
