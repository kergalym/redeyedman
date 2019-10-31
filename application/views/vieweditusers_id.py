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

from application.core.datalogics import Utils
from application import app
from application import sql
from application.core.dbmodel import Users
from application.core.dbmodel import Categories
from application.core.datalogics import SysInfo
from application.forms import userspage_idform
from application.forms import genpassform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify
from flask import g
from sqlalchemy import exc


@app.route('/adminboard/editpage_id_users/<int:id>', methods=['GET', 'POST'])
@login_required
def show_userspageid(id):
    form = userspage_idform.UsersidForm()
    editpage_output_loop = Users.query.filter_by(id=id).first()
    categories_loop = Categories.query.all()
    instance = SysInfo()
    atime = instance.altertime()
    author = g.user

    if (editpage_output_loop
            and categories_loop
            and atime
            and author is not None):
        return render_template(
            'adminboard/editpage_id_users.html',
            atime=atime,
            editpage_output_loop=editpage_output_loop,
            form=form)
    else:
        return redirect(url_for('show_login'))


@app.route('/adminboard/editpage_id_users/', methods=['GET', 'POST'])
@login_required
def update_userspageid():
    form = userspage_idform.UsersidForm()
    form_genpass = genpassform.DashboardGenPassForm()
    utils = Utils()
    author = g.user

    if (author is not None
            and request.method == 'POST'
            and request.form.get('save', None)
            and form.validate_on_submit()):
        id = request.form['id']
        login = request.form['login']
        password = utils.hash_password(request.form['password'])
        email = request.form['email']
        regdate = request.form['regdate']
        usr_level = request.form['usr_level']
        usersdata = Users(id, login, password, email,
                          regdate, usr_level)
        sql.session.add(usersdata)
        try:
            sql.session.commit()
            flash("User's data is changed", 'info')
        except exc.IntegrityError:
            flash("Identical user's data is exist", 'error')
        flash("User's data is changed", 'info')
        return redirect(url_for('show_userspageid',
                                id=form.id.data))
    elif author is not None \
            and request.method == 'POST' \
            and form_genpass.validate_on_submit():
        passwordphrase = utils.randomstr(int(request.form['passlength']))
        return jsonify(passwordphrase=passwordphrase)
    else:
        flash("User's data is not changed", 'error')
        return redirect(url_for('show_userspageid',
                                id=form.id.data))
    return render_template('adminboard/editpage_id_users.html',
                           form=form)
