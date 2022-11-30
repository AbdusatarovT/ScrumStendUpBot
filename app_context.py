from flask import  Flask
from flask_cors import CORS
from db_home.models import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


__author__ = 'Tahir'


def create_app(config='configuration'):
    app = Flask(__name__)

    app.config.from_object(config)

    migrate = Migrate()
    CORS(app, headers=['Content-Type', 'Authorization'])

    db.init_app(app)
    migrate.init_app(db=db, app=app)

    # Register blueprints
    from db_home import home_route
    app.register_blueprint(home_route, url_prefix='/')

    return app
