from datetime import datetime
from db_home.models import User, Task
from db_home.models import db
from admin_app import app



def get_users_list():
    """Метод для полученя списка пользователей и их ID"""
    with app.app_context():
        username_and_id = db.session.query(User.tg_username, User.id).all()
        return username_and_id


def get_user_db(username):
    """Метод для проверки поьзователя в БД"""
    with app.app_context():
        tg_name = db.session.query(User.tg_username, User.id).filter(User.tg_username == username).first()
        return tg_name

def add_new_task(user_id, user_tg_id):
    """Метод для создания нового таска"""
    with app.app_context():
        task = Task()
        task.user_id = user_id
        task.tg_id = user_tg_id
        db.session.add(task)
        db.session.commit()

