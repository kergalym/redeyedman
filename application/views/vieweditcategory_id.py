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
from application.forms import categorypage_idform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from sqlalchemy import exc


@app.route('/adminboard/editpage_id_category/<int:id>', methods=['GET', 'POST'])
@login_required
def show_categorypageid(id):
    form = categorypage_idform.CategorypageidForm()
    editpage_output_loop = Categories.query.filter_by(id=id).first()
    instance = SysInfo()
    atime = instance.altertime()
    author = session['login']
    if (editpage_output_loop
            and atime
            and author is not None):
        return render_template(
            'adminboard/editpage_id_category.html',
            author=author, atime=atime,
            editpage_output_loop=editpage_output_loop,
            form=form)
    else:
        return redirect(url_for('show_login'))


@app.route('/adminboard/editpage_id_category/', methods=['GET', 'POST'])
@login_required
def update_categorypageid():
    error = None
    form = categorypage_idform.CategorypageidForm()
    author = session['login']
    if request.method == 'POST' and form.validate_on_submit():
        if author is not None:
            category_id = request.form['category_id']
            category_title = request.form['category_title']
            category_author = request.form['category_author']
            category_date = request.form['category_date']
            category_desc = request.form['category_desc']
            categories = Categories(category_id, category_title,
                                    category_author, category_date, category_desc)
            sql.session.add(categories)
            try:
                sql.session.commit()
                flash("Category is changed", 'info')
            except exc.IntegrityError:
                flash("Category with same name is exist", 'error')
            return redirect(url_for('show_categorypageid',
                                    category_id=request.form['category_id']))
    else:
        flash("Category is not changed", 'error')
        return redirect(url_for('show_categorypageid'))
    return render_template('adminboard/editpage_id_category.html',
                           form=form, error=error
                           )
