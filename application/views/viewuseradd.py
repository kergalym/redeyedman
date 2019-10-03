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

from application import app
from application import sql
from application.core.dbmodel import Users
from application.core.datalogics import Utils
from application.forms import useraddform
from flask_login import login_required
from flask import render_template
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import g


#
#   USER ADD MENU
#

@app.route('/adminboard/', methods=['GET', 'POST'])
# @app.route('/adminboard/adminboard_main/', methods=['GET', 'POST'])
# @app.route('/adminboard/adminboard_inner/', methods=['GET', 'POST'])
# @app.route('/adminboard/adminboard_category/', methods=['GET', 'POST'])
# @app.route('/adminboard/adminboard_users/', methods=['GET', 'POST'])
# @app.route('/adminboard/adminboard_settings/', methods=['GET', 'POST'])
@login_required
def useradd():
    form = useraddform.UserAddForm()
    utils = Utils()
    author = g.user
    if (request.method == 'POST' and author is not None
            and request.form['user_submit']
            and form.validate_on_submit()):
        rows = sql.session.query(Users).count()
        if type(rows) == int:
            id = rows + 1
            login = form.login.data
            usr_lvl = form.usr_lvl.data
            email = form.email.data
            regdate = form.regdate.data
            password = utils.hash_password(form.password.data)
            userdata = Users(id, login, password,
                             email, regdate, usr_lvl)
            sql.session.add(userdata)
            sql.session.commit()
            flash("User" + login + "is added", 'info')
        return redirect(url_for('show_dashboard'))
    else:
        flash("User" + form.login.data + "is not added", 'error')
        return redirect(url_for('show_dashboard'))
    return render_template('adminboard/adminboard.html',
                           form=form
                           )
