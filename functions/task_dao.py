from db_home.models import User, Task
from db_home.models import db
from admin_app import app
from datetime import datetime


def get_my_info(id):
    """Метод для получения истории задач пользователя"""
    with app.app_context():
        res = db.session.query(Task).filter(Task.tg_id == id).order_by(Task.id.desc()).limit(5).all()
        return res


def get_tasks_user_id():
    """Метод для получения списка ID пользователей"""
    with app.app_context():
        task = db.session.query(Task.user_id).all()
        list_id = []
        for i in task:
            list_id.append(i[0])
        return list_id


def get_friends_task(id):
    """Метод для получния последних текущих коллег"""
    with app.app_context():
        try:
            list_id = get_tasks_user_id()
            if id in list_id:
                tasks = db.session.query(Task.yesterday_task, Task.today_task, Task.problem, Task.user_id, Task.date)\
                    .filter(Task.user_id == id).order_by(Task.id.desc()).limit(1).all()
                task_date = tasks[0]['date'].strftime("%d.%m.%Y")
                date_now = datetime.now().strftime("%d.%m.%Y")
                if date_now == task_date:
                    return tasks[0]
                elif date_now != task_date:
                    return 1
            else:
                return None
        except Exception as e:
            return e



def get_my_lust_task(user_id):
    """Метод для получения истории задач пользователя"""
    with app.app_context():
        a = db.session.query(Task.yesterday_task, Task.today_task, Task.problem, Task.user_id, Task.date, Task.id)\
                    .filter(Task.tg_id == user_id).order_by(Task.id.desc()).limit(1).all()
        task_date = a[0]['date'].strftime("%d.%m.%Y")
        date_now = datetime.now().strftime("%d.%m.%Y")
        if date_now == task_date:
            return a[0]['id']
        elif date_now != task_date:
            return None


def add_first_answer(task_id, text):
    """Метод для добавления yesterday_task"""
    with app.app_context():
        a = db.session.query(Task).filter(Task.id == task_id).first()
        a.yesterday_task = text
        db.session.add(a)
        db.session.commit()


def add_second_answer(task_id, text):
    """Метод для добавления today_task"""
    with app.app_context():
        a = db.session.query(Task).filter(Task.id == task_id).first()
        a.today_task = text
        db.session.add(a)
        db.session.commit()


def add_third_answer(task_id, text):
    """Метод для добавления problem"""
    with app.app_context():
        a = db.session.query(Task).filter(Task.id == task_id).first()
        a.problem = text
        db.session.add(a)
        db.session.commit()