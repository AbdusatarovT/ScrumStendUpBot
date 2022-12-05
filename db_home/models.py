from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship


__author__ = 'Tahir'

db = SQLAlchemy()

# class Permission:
#     CREATE_TICKET = 1
#     READ_TICKET = 2
#     UPDATE_TICKET = 3
#     DELETE_TICKET = 4
#     ADD_COMMENT = 10
#     EDIT_COMMENT = 11
#     DELETE_COMMENT = 12


class User(db.Model):
    """Модель таблицы 'Пользователей'"""
    __tablename__ = 'user'

    id = db.Column(Integer, primary_key=True)
    tg_username = db.Column(String(65), unique=True, nullable=False)
    fullname = db.Column(String(80), unique=True)
    email = db.Column(String(65), unique=True, nullable=False)
    password = db.Column(String(160))
    avatar = db.Column(String(255))
    tasks = db.relationship('Task', backref='task', lazy='dynamic')

    def create_user_password_hash(self, user_password):
        """Метод для хеширования пароля"""
        self.password = generate_password_hash(user_password)

    @staticmethod
    def check_user_password_hash(self, user_password):
        """Метод для прверки хешированного пароля"""
        return check_password_hash(self.password, user_password)



class Task(db.Model):
    """Модель таблицы 'Задач'"""
    __tablename__ = 'task'

    id = db.Column(Integer, primary_key=True)
    tg_id = db.Column(Integer)
    yesterday_task = db.Column(Text)
    today_task = db.Column(Text)
    problem = db.Column(Text)
    date = db.Column(DateTime, default=datetime.now())
    user_id = db.Column(Integer,ForeignKey('user.id'))
    








# class Role():
#     __tablename__ = 'role'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(65))


# class Role(db.Model):
#     __tablename__ = 'role'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')

#     def init(self, **kwargs):
#         super(Role, self).init(**kwargs)
#         if self.permissions is None:
#             self.permissions = 0

#     @staticmethod
#     def insert_roles():
#         roles = {
#             'Developer': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
#             'Moderator': [Permission.FOLLOW, Permission.COMMENT,
#                           Permission.WRITE, Permission.MODERATE],
#             'Administrator': [Permission.FOLLOW, Permission.COMMENT,
#                               Permission.WRITE, Permission.MODERATE,
#                               Permission.ADMIN],
#         }
#         default_role = 'Developer'
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.reset_permissions()
#             for perm in roles[r]:
#                 role.add_permission(perm)
#             role.default = (role.name == default_role)
#             db.session.add(role)
#         db.session.commit()

#     def add_permission(self, perm):
#         if not self.has_permission(perm):
#             self.permissions += perm

#     def remove_permission(self, perm):
#         if self.has_permission(perm):
#             self.permissions -= perm

#     def reset_permissions(self):
#         self.permissions = 0

#     def has_permission(self, perm):
#         return self.permissions & perm == perm

#     def repr(self):
#         return f'<Role {self.name}>'
