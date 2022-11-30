from app_context import create_app
from flask_migrate import MigrateCommand
from flask_script import Manager
from db_home.models import db, User

__author__ = 'Tahir'

app = create_app()
manager = Manager(app, db)
manager.add_command('db', MigrateCommand)

# @app.shell_context_processor
# def make_shell_context():
#     return dict(app=app, db=db, User=User)

if __name__ == '__main__':
    manager.run()
