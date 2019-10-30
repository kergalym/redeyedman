# -*- coding: utf-8 -*-

# Copyright (C) 2017 Galym Kerimbekov <kegalym2@mail.ru>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from os import remove
from os.path import exists, isfile
from application import app
from application import sql
from application import session
from application import session_timein
from application import bcrypt
from application import login_manager
from application.core.dbmodel import Users
from application.forms import loginform
from flask import session as session
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import g
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from functools import wraps


@app.route('/login/', methods=['GET', 'POST'])
def show_login():
    form = loginform.LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = sql.session.query(Users).filter_by(
            login=form.login.data
        ).first()
        if user is not None and \
            bcrypt.check_password_hash(
                user.password,
                form.password.data):
            session['SECRET_KEY'] = True
            session['login'] = user.login
            login_user(user)
            return redirect(url_for('show_dashboard'))
        else:
            flash('Invalid login or password.', 'error')
    return render_template('adminboard/login.html', form=form)


login_manager.login_view = 'show_login'


@app.before_request
def load_user():
    g.user = None
    if 'login' in session:
        user = sql.session.query(Users).filter_by(
            login=session["login"]).first()
        g.user = user.login

    session.permanent = True

    if session_timein == 0:
        session.clear()
        return redirect(url_for('show_login', next=request.url))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('show_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/logout/')
@login_required
def user_logout():
    logout_user()
    session.clear()
    if (exists(("{}/static/get_path.tmp".format(app.root_path)))
            and isfile(("{}/static/get_path.tmp".format(app.root_path)))):
        remove("{}/static/get_path.tmp".format(app.root_path))
    return redirect(url_for('show_login'))
