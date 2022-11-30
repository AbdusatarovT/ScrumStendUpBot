import os

POSTGRES = {
    'user': 'tahir',
    'pw': '123',
    'db': 'scrum_bot',
    'host': 'localhost',
    'port': '5432',
}
SECRET_KEY = 'qwlkdjqwdioqjiod8o1eu1892e71289718euovh07980ey2v89ry023r$@#$!@#$!$@#!*@%*!%'
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = False
BOT_TOKEN = '5806246043:AAEChMTY0BJZ-a84T00ntXkP9BBRVygWjR0'
BASE_DIR = os.path.abspath('.')
UPLOAD_FOLDER = 'avatars'
DEBUG=True