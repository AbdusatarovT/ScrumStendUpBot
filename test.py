
from db_home.models import User, Task
from db_home.models import db
from admin_app import app





def get_info():
    with app.app_context():
        a = db.session.query(Task).filter(Task.tg_id == 185548016).order_by(Task.id.desc()).limit(5).all()
        for i in a:
            print(i.yesterday_task)

# get_info()