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


@app.route('/adminboard/useradd', methods=['GET', 'POST'])
@login_required
def useradd():
    form = useraddform.UserAddForm()
    utils = Utils()
    author = g.user

    if (request.method == 'POST' and author is not None
            and form.user_submit.data
            and form.validate_on_submit()):

        rows = sql.session.query(Users).count()
        if type(rows) == int:
            id = rows + 1
            login = form.login.data
            usr_lvl = form.usr_lvl.data
            email = form.email.data
            regdate = request.form['regdate']
            password = utils.hash_password(form.password.data)
            userdata = Users(id, login, password,
                             email, regdate, usr_lvl)

            sql.session.add(userdata)
            sql.session.commit()
            flash("User {} is added".format(login), 'info')
            return redirect(url_for('show_dashboard_users'))
        else:
            flash("User {} is not added. {}".format(form.login.data, form.errors), 'error')
            return redirect(url_for('show_dashboard_users'))

    return render_template('adminboard/adminboard_users.html',
                           form=form
                           )
