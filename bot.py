import requests
import telebot
import time
import schedule
from threading import Thread
from configuration import BOT_TOKEN
from db_home.models import User, Task
from db_home.models import db
from admin_app import app
from functions.task_dao import *
from functions.user_dao import  *



bot = telebot.TeleBot(BOT_TOKEN)




def send_msg():
    """Метод для ежедневный рассылок"""
    text = "Добрый день! Заполни отчет!\nПереходи по ссылке: https://t.me/ScrumStandUp_Bot"
    token = BOT_TOKEN
    chat_id = "-1001799419976"  # ID тестового чата
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
    results = requests.get(url_req)
    print(results.json())


@bot.message_handler(commands=['info'])
def get_info(message):
    """Команда для получения истории задач"""
    with app.app_context():
        last_tasks = get_my_info(message.from_user.id)
        try:
            for i in last_tasks:
               bot.send_message(message.chat.id, \
                f'Вчерашний таск: {i.yesterday_task}\nСегоднешний таск: {i.today_task}\nПроблемы: {i.problem}\nДата: {i.date.strftime("%d.%m.%Y %H:%M")}')
        except IndexError:
            bot.send_message(message.chat.id,'Друг что то пошло не так, давай попробуем еще раз!')


@bot.message_handler(commands=['update_task'])
def update_task(message):
    with app.app_context():
        task_id = get_my_lust_task(message.from_user.id)
        if task_id != None:
            bot.send_message(message.chat.id,'Какую задачу ты будешь делать сегодня?')
            bot.register_next_step_handler(message, add_second_question, task_id=task_id)
        else:
            bot.send_message(message.chat.id,'Вы сегодня не проходили опрос!😱\n Необходимо пройти опрос!📜')


@bot.message_handler(commands=['friends_task'])
def get_last_friends_task(message):
    """Команда для просмотра последниз задач у колег"""
    with app.app_context():
        try:
            username = get_users_list()
            for i in username:
                if message.from_user.username != i[0]:
                    tasks = get_friends_task(i[1])
                    if tasks == 1:
                        bot.send_message(message.chat.id,f'У {i[0]} на сегоня нет задач')
                        break
                    bot.send_message(message.chat.id,\
                        f'Username: {i[0]}\nВчерашний таск: {tasks.yesterday_task}\nСегоднешний таск:\
                             {tasks.today_task}\nПроблемы:{tasks.problem}')
        except Exception:
            bot.send_message(message.chat.id,'Друг что то пошло не так, давай попробуем еще раз!😱')


@bot.message_handler(commands=['start'])
def cheak_yourself(message):
    """Метод для проверки пользователя"""
    with app.app_context():
        task_id = get_my_lust_task(message.from_user.id)
        if task_id == None:
            user_name_id = get_user_db(message.from_user.username)
            if message.from_user.username == user_name_id[0]:
                bot.send_message(message.chat.id, 'Добрый день шеф 🌞\nКакую задачу ты делал вчера?🧐')
                task = Task()
                task.user_id = user_name_id[1]
                task.tg_id = message.from_user.id
                db.session.add(task)
                db.session.commit()
                bot.register_next_step_handler(message, add_first_question, task_id=task.id)
            else:
                bot.send_message(message.chat.id, 'Не прошел Васек!')
        else:
            bot.send_message(message.chat.id, 'Вы сегодня проходили опрос!\nВы можете изменить текущую задачу и проблему вызвав команду /update_task')
            


##### Ветка общения с пользователем #####

def add_first_question(message, **kwargs):
    """Ответ на первый вопрос. Ответ сохранен в базе данных"""
    with app.app_context():
        print(kwargs)
        print(message.text)
        try:
            task_id = kwargs.get('task_id', None)
            if task_id and task_id is not None:
                add_first_answer(task_id, message.text)
            bot.send_message(message.chat.id, 'Какую задачу ты будешь делать сегодня?🤓')
            bot.register_next_step_handler(message, add_second_question, task_id=task_id)
        except Exception:
            bot.register_next_step_handler('Друг что то пошло не так, давай попробуем еще раз!\nКакую задачу ты делал вчера?', \
                add_first_question, task_id=task_id)


def add_second_question(message, **kwargs):
    """Ответ на второй вопрос."""
    with app.app_context():
        print(kwargs)
        print(message.text)
        try:
            task_id = kwargs.get('task_id', None)
            if task_id and task_id is not None:
                add_second_answer(task_id, message.text)
            bot.send_message(message.chat.id, 'Какие у тебя возникли проблемы?')
            bot.register_next_step_handler(message, add_problems, task_id=task_id)
        except Exception:
            bot.register_next_step_handler('Друг что то пошло не так, давай попробуем еще раз!\nКакую задачу ты будешь делать сегодня?', \
                add_second_question, task_id=task_id)


def add_problems(message, **kwargs):
    """Ответ на третий вопрос."""
    with app.app_context():
        print(kwargs)
        print(message.text)
        try:
            task_id = kwargs.get('task_id', None)
            if task_id and task_id is not None:
                add_third_answer(task_id, message.text)
            bot.send_message(message.chat.id, 'Опрос успешно пройден! До завтра 🖖🏽')
        except Exception:
            bot.register_next_step_handler('Друг что то пошло не так, давай попробуем еще раз!\nКакие у тебя возникли проблемы?', \
                add_problems, task_id=task_id)



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



