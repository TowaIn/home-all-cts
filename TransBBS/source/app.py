# app.py
# -*- coding: utf-8 -*-

import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from markupsafe import Markup, escape
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

app = Flask(__name__)

app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'key')
BBS_PASSWORD = os.environ.get('BBS_PASSWORD', 'password')

posts = []
post_id_counter = 0

def nl2br(value):
    """改行文字を<br>タグに変換するカスタムフィルタ"""
    if value:
        escaped_value = escape(value)
        formatted_value = escaped_value.replace('\r\n', '<br>\n').replace('\r', '<br>\n').replace('\n', '<br>\n')
        return Markup(formatted_value)
    return ""

app.jinja_env.filters['nl2br'] = nl2br

pygments_formatter = HtmlFormatter(linenos=True, cssclass="codehilite", style='default')
pygments_css = pygments_formatter.get_style_defs('.codehilite')


def login_required(f):
    """ログイン状態をチェックし、未ログインならログインページへリダイレクト"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('この操作を行うにはログインが必要です。', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """投稿一覧を表示する"""
    return render_template('index.html', posts=reversed(posts), pygments_css=pygments_css)

@app.route('/post', methods=['POST'])
@login_required # 書き込みはログイン必要
def post():
    """新しい投稿を受け付ける"""
    global post_id_counter
    username = request.form.get('username', '名無しさん')
    message = request.form.get('message')
    code_snippet = request.form.get('code_snippet')
    language = request.form.get('language', 'text')
    highlighted_code = None

    if code_snippet:
        try:
            lexer = get_lexer_by_name(language, stripall=True)
        except ClassNotFound:
            lexer = get_lexer_by_name('text', stripall=True)
        highlighted_code = highlight(code_snippet, lexer, pygments_formatter)

    if message or code_snippet:
        post_id_counter += 1
        posts.append({
            'id': post_id_counter,
            'username': username if username else '名無しさん',
            'message': message,
            'highlighted_code': highlighted_code
        })

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン処理を行う"""
    if session.get('logged_in'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        password_attempt = request.form.get('password')
        if password_attempt == BBS_PASSWORD:
            session['logged_in'] = True
            flash('ログインしました。', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('index'))
        else:
            flash('パスワードが間違っています。', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    """ログアウト処理を行う"""
    session.pop('logged_in', None)
    flash('ログアウトしました。', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
