# app/routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db, login_manager
from app.models import User, Chat, Message
from app.forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .api import get_completion, summarize
import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('登录成功！', 'success')
            return redirect(url_for('chat'))
        else:
            flash('登录失败，请检查用户名和密码', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/chat', methods=['GET'])
@login_required
def chat():
    return render_template('chat.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/api/chats', methods=['GET'])
@login_required
def get_chats():
    chats = Chat.query.filter_by(user_id=current_user.id).all()
    return jsonify([
        {
            'id': chat.id,
            'context': chat.context,
        }
        for chat in chats
    ])


@app.route('/api/chats', methods=['POST'])
@login_required
def create_chat():
    chat = Chat(user_id=current_user.id, timestamp=datetime.datetime.now(), context='', is_complete=True)
    db.session.add(chat)
    db.session.commit()
    return jsonify({
        'id': chat.id,
        'context': chat.context,
    })


@app.route('/api/chats/<int:chat_id>/messages', methods=['GET'])
@login_required
def get_messages(chat_id):
    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first()
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404

    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.timestamp).all()
    return jsonify([
        {
            'role': 'User' if message.user_id == current_user.id else 'AI',
            'content': message.text,
        }
        for message in messages
    ])


@app.route('/api/chats/<int:chat_id>/messages', methods=['POST'])
@login_required
def send_message(chat_id):
    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first()

    if not chat:
        return jsonify({'error': 'Chat not found'}), 404

    message_text = request.json.get('content')
    if not message_text:
        return jsonify({'error': 'Message cannot be empty'}), 400

    # 将用户消息存储到数据库中
    user_message = Message(chat_id=chat_id, user_id=current_user.id, text=message_text, is_response=False,
                           timestamp=datetime.datetime.now())
    db.session.add(user_message)
    db.session.commit()

    # 获取 AI 回复
    ai_response = get_completion(message_text)

    # 将 AI 消息存储到数据库中
    ai_message = Message(chat_id=chat_id, user_id=None, text=ai_response, is_response=True,
                         timestamp=datetime.datetime.now())
    db.session.add(ai_message)
    db.session.commit()

    # 如果聊天的context字段为空
    if not chat.context:
        chat.context = summarize(message_text)
        db.session.commit()

    return jsonify({
        'role': 'AI',
        'content': ai_response,
        'context': chat.context
    })

@app.route('/api/chats/<int:chat_id>', methods=['DELETE'])
@login_required
def delete_chat(chat_id):
    chat = Chat.query.filter_by(id=chat_id, user_id=current_user.id).first()
    if not chat:
        return jsonify({'error': 'Chat not found'}), 404

    # 删除所有相关的消息
    Message.query.filter_by(chat_id=chat_id).delete()

    # 删除聊天
    db.session.delete(chat)
    db.session.commit()

    return jsonify({'message': 'Chat deleted'}), 200
