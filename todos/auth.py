import functools

from flask import (
    Blueprint, flash, g, render_template, url_for, request, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute('SELECT id FROM users WHERE username = %s', (username,))

        if not username:
            error = "Usuario es requerido"
        if not password:
            error = "Password es requerido"
        elif c.fetchone() is not None:
            error = f"Ususario {username} se encuentra registrado."

        if error is None:
            c.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                      (username, generate_password_hash(password, salt_length=99)))
            db.commit()

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute('SELECT * FROM users WHERE username = %s', (username, ))

        user = c.fetchone()

        if user is None:
            error = "Usuario y/o Contraseña invalido."
        elif not check_password_hash(user['password'], password):
            error = "Usuario y/o Contraseña invalido."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_loged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute('SELECT * FROM users WHERE id = %s', (user_id, ))
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapper_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapper_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
