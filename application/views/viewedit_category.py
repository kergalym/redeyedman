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
from application.core.dbmodel import Categories
from application.core.datalogics import SysInfo
from application.forms import categorypageform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from sqlalchemy import exc


@app.route('/adminboard/editpage_category/')
@login_required
def show_editpage_category():
    form = categorypageform.CategorypageAddForm()
    editpage_output_loop = Categories.query.filter_by(
        category_author='admin'
    ).first()
    instance = SysInfo()
    atime = instance.altertime()
    author = g.user
    if (editpage_output_loop
            and atime
            and author is not None):
        return render_template('adminboard/editpage_category.html',
                               author=author, atime=atime,
                               editpage_output_loop=editpage_output_loop,
                               form=form
                               )
    else:
        return redirect(url_for('show_login'))


@app.route('/adminboard/editpage_category/', methods=['GET', 'POST'])
@login_required
def add_editpage_category():
    form = categorypageform.CategorypageAddForm()
    author = g.user
    iid = None
    if (request.method == 'POST'
            and request.form['save']
            and author is not None
            and form.validate_on_submit()):
        rows = sql.session.query(Categories).count()
        if type(rows) == int:
            iid = rows + 1
        category_title = request.form['category_title']
        category_author = request.form['category_author']
        category_date = request.form['category_date']
        category_desc = request.form['category_desc']
        categories = Categories(iid, category_title, category_author,
                                category_date, category_desc)
        sql.session.add(categories)
        try:
            sql.session.commit()
            flash("Category is added", 'info')
        except exc.IntegrityError:
            flash("Category {} is exist".format(category_title), 'error')
        return redirect(url_for('show_dashboard_category'))
    else:
        flash("Category is not added", 'error')
        return redirect(url_for('show_dashboard_category'))
    return render_template('adminboard/editpage_category.html',
                           form=form
                           )
