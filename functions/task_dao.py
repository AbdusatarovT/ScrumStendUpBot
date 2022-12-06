from db_home.models import User, Task
from db_home.models import db
from datetime import date
from sqlalchemy import func

def get_my_info(id):
    """Метод для получения истории задач пользователя"""
    res = db.session.query(Task).filter(Task.tg_id == id).order_by(Task.id.desc()).limit(5).all()
    return res


def get_tasks_user_id():
    """Метод для получения списка ID пользователей"""
    task = db.session.query(Task.user_id).all()
    list_id = []
    for i in task:
        list_id.append(i[0])
    return list_id


def get_friends_task():
    """Метод для получния последних текущих коллег"""
    query = db.session.query(User, Task).join(Task).filter(func.date(Task.date)==date.today()).all()
    return query


def get_my_lust_task(id):
    """Метод для получения истории задач пользователя"""
    query = db.session.query(User, Task).join(Task).filter(func.date(Task.date)==date.today()).filter(Task.tg_id == id).all()
    for user, task in query:
        return task.id


def add_first_answer(task_id, text):
    """Метод для добавления yesterday_task"""
    a = db.session.query(Task).filter(Task.id == task_id).first()
    a.yesterday_task = text
    db.session.add(a)
    db.session.commit()


def add_second_answer(task_id, text):
    """Метод для добавления today_task"""
    a = db.session.query(Task).filter(Task.id == task_id).first()
    a.today_task = text
    db.session.add(a)
    db.session.commit()


def add_third_answer(task_id, text):
    """Метод для добавления problem"""
    a = db.session.query(Task).filter(Task.id == task_id).first()
    a.problem = text
    db.session.add(a)
    db.session.commit()