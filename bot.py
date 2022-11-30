import requests
import telebot
import time
import schedule
from threading import Thread
from configuration import BOT_TOKEN
from db_home.models import User, Task
from db_home.models import db
from admin_app import app



bot = telebot.TeleBot(BOT_TOKEN)




def send_msg():
    """Метод для ежедневный рассылок"""
    text = "Добрый день! Заполни отчет!\nПереходи по ссылке: https://t.me/ScrumStandUp_Bot"
    token = BOT_TOKEN
    chat_id = "-1001799419976"  # ID тестового чата
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
    results = requests.get(url_req)
    print(results.json())


@bot.message_handler(commands=['start'])
def start(message):
    """Команда для запуска бота"""
    bot.send_message(message.chat.id, 'Доброе утро! Давай поболтаем, введи свой Username!')


@bot.message_handler(commands=['info'])
def get_info(message):
    """Команда для получения истории задач"""
    with app.app_context():
        a = db.session.query(Task).filter(Task.tg_id == message.from_user.id).order_by(Task.id.desc()).limit(5).all()
        try:
            for i in a:
               bot.send_message(message.chat.id, f'Вчерашний таск: {i.yesterday_task}\nСегоднешний таск: {i.today_task}\nДата: {i.date}')
        except IndexError:
            bot.send_message(message.chat.id,'Друг что то пошло не так, давай попробуем еще раз!')


@bot.message_handler(commands=['friends_task'])
def friends_task(message):
    """Команда для просмотра последниз задач у колег"""
    with app.app_context():
        try:
            username = db.session.query(User.tg_username, User.id).all()
            for i in username:
                if i.tg_username == message.from_user.username:
                    continue
                tasks = db.session.query(Task.yesterday_task, Task.today_task, Task.problem, Task.user_id).filter(Task.user_id ==i.id)[-1]
                bot.send_message(message.chat.id, f'Username: {i.tg_username}\nВчерашний таск: {tasks.yesterday_task}\nСегоднешний таск: {tasks.today_task}\nПроблемы:{tasks.problem}')
        except Exception:
            bot.register_next_step_handler('Друг что то пошло не так, давай попробуем еще раз!', friends_task)



@bot.message_handler(content_types=['text'])
def cheak_yourself(message):
    """Метод для проверки пользователя"""
    with app.app_context():
        tg_name = db.session.query(User.tg_username).filter(User.tg_username == message.from_user.username).first()
        user_id = db.session.query(User.id).filter(User.tg_username == message.from_user.username).first()
        tg_id = message.from_user.id
        if message.text == tg_name['tg_username']:
            bot.send_message(message.chat.id, 'Окей красавчик!')
            bot.send_message(message.chat.id, 'Какую задачу ты делал вчера?')
            task = Task()
            task.user_id = user_id['id']
            task.tg_id = tg_id
            db.session.add(task)
            db.session.commit()
            db.session.flush()
            bot.register_next_step_handler(message, first_question, task_id=task.id)
        else:
            bot.send_message(message.chat.id, 'Не прошел Васек!')

##### Ветка общения с пользователем #####

def first_question(message, **kwargs):
    """Ответ на первый вопрос. Ответ сохранен в базе данных"""
    with app.app_context():
        print(kwargs)
        print(message.text)
        try:
            task_id = kwargs.get('task_id', None)
            if task_id and task_id is not None:
                first_answer = message.text
                a = db.session.query(Task).filter(Task.id == task_id).first()
                a.yesterday_task = first_answer
                db.session.add(a)
                db.session.commit()
            bot.send_message(message.chat.id, 'Какую задачу ты будешь делать сегодня?')
            bot.register_next_step_handler(message, second_question, task_id=a.id)
        except Exception:
            bot.register_next_step_handler('Друг что то пошло не так, давай попробуем еще раз! Какую задачу ты делал вчера?', first_question, task_id=a.id)


def second_question(message, **kwargs):
    """Ответ на второй вопрос."""
    with app.app_context():
        print(kwargs)
        print(message.text)
        try:
            task_id = kwargs.get('task_id', None)
            if task_id and task_id is not None:
                second_answer = message.text
                a = db.session.query(Task).filter(Task.id == task_id).first()
                a.today_task = second_answer
                db.session.add(a)
                db.session.commit()
            bot.send_message(message.chat.id, 'Какие у тебя возникли проблемы?')
            bot.register_next_step_handler(message, problems, task_id=a.id)
        except Exception:
            bot.register_next_step_handler('Друг что то пошло не так, давай попробуем еще раз! Какую задачу ты будешь делать сегодня?', second_question, task_id=a.id)


def problems(message, **kwargs):
    """Ответ на третий вопрос."""
    with app.app_context():
        print(kwargs)
        print(message.text)
        try:
            task_id = kwargs.get('task_id', None)
            if task_id and task_id is not None:
                problem = message.text
                a = db.session.query(Task).filter(Task.id == task_id).first()
                a.problem = problem
                db.session.add(a)
                db.session.commit()
            bot.send_message(message.chat.id, 'Опрос успешно пройден! До завтра 🖖🏽')
        except Exception:
            bot.register_next_step_handler('Друг что то пошло не так, давай попробуем еще раз! Какие у тебя возникли проблемы?', problems, task_id=a.id)



def do_schedule():
    """Метод для запуска обработчика задач"""
    # schedule.every(10).seconds.do(send_msg)
    schedule.every().day.at("10:00").do(send_msg)

    while True:
        schedule.run_pending()
        time.sleep(1)


def main_loop():
    """Разделения работы бота на потоки. Один поток отвечает за отправку ежедневных сообщений.
        Второй поток отвечает за работу бота"""
    thread = Thread(target=do_schedule)
    thread.start()

    bot.polling(True)


if __name__ == '__main__':
    main_loop()



