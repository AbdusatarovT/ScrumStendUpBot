import os
from . import home_route
from flask import request, jsonify, current_app
from .models import User, db
from werkzeug.utils import secure_filename


@home_route.route('/create_user', methods=['POST'])
def home():
    '''
        {
            "tg_username": "tahir1",
            "email": "tahir1@t.com"
        }
    '''
    user_data = request.get_json()

    tg_username = user_data.get('tg_username', None)
    email = user_data.get('email', None)
    password = user_data.get('password', None)

    check_tg_username = User.query.filter_by(tg_username=tg_username).first()
    check_user_email = User.query.filter_by(email=email).first()

    if check_tg_username:
        return jsonify(error='Пользователь уже существует')

    if check_user_email:
        return jsonify(error='Почта занята')
    
    # if not password:
    #     return jsonify(error='Пожалуйста введите пароль')
    
    create_new_user = User()
    create_new_user.tg_username = tg_username
    create_new_user.email = email
    # create_new_user.create_user_password_hash(password)

    db.session.add(create_new_user)
    db.session.commit()

    return jsonify(test='Hello'), 200


@home_route.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    username = request.form.get('username')
    get_file = request.files['avatar']
    base_dir = current_app.config['BASE_DIR'] 
    upload_folder = current_app.config['UPLOAD_FOLDER']
    full_direction = os.path.join(base_dir, upload_folder)

    get_user = User.query.filter_by(tg_username=username).first()

    if not get_user:
        return jsonify(test='Пользователь не найден'), 500

    if not os.path.exists(upload_folder):
        os.makedirs(full_direction)

    file_is_secure = secure_filename(get_file.filename)
    get_file_extension = os.path.splitext(get_file.filename)[1]

    if file_is_secure:
        if get_file_extension in ['.png', '.jpg', '.jpeg']:
            avatar_path = f'{full_direction}/{get_file.filename}'
            avatar_user_path = f'{upload_folder}/{get_file.filename}'
            get_file.save(avatar_path)
            get_user.avatar = avatar_user_path
            db.session.commit()
        else:
            return jsonify(test='Формат не поддердивается'), 500

    return jsonify(test='Upload avatar'), 200
