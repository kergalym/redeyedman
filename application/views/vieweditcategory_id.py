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
from application import engine
from application import sql
from sqlalchemy import update
from application.core.dbmodel import Categories
from application.core.datalogics import SysInfo
from application.forms import categorypage_idform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from sqlalchemy import exc


@app.route('/adminboard/editpage_id_category/<int:id>', methods=['GET', 'POST'])
@login_required
def show_categorypageid(id):
    form = categorypage_idform.CategorypageidForm()
    editpage_output_loop = sql.session.query(Categories).filter_by(id=id).first()
    instance = SysInfo()
    atime = instance.altertime()
    author = g.user
    if (editpage_output_loop
            and atime
            and author is not None):
        return render_template(
            'adminboard/editpage_id_category.html',
            editpage_output_loop=editpage_output_loop,
            form=form)
    else:
        return redirect(url_for('show_login'))


@app.route('/adminboard/editpage_id_category/', methods=['GET', 'POST'])
@login_required
def update_categorypageid():
    error = None
    form = categorypage_idform.CategorypageidForm()
    instance = SysInfo()
    author = g.user

    if (request.method == 'POST' and author is not None
            and request.form['save']):
        if form.validate_on_submit():

            # if author field is suddenly empty
            form.category_author.data = unicode(author)

            # we assign record time to this form element
            # as unicode string to be consistent with other form elements here
            form.category_date.data = unicode(instance.altertime())

            conn = engine.connect()
            stmt = update(Categories).where(
                Categories.id == form.id.data).values(
                id=form.id.data,
                category_title=form.category_title.data,
                category_author=form.category_author.data,
                category_date=form.category_date.data,
                category_desc=form.category_desc.data
            )

            try:
                conn.execute(stmt)
                flash("Category is changed", 'info')
            except exc.IntegrityError:
                flash("Category with same name is exist", 'error')
            return redirect(url_for('show_categorypageid',
                                    id=form.id.data))
    else:
        flash("Category is not changed", 'error')
        return redirect(url_for('show_categorypageid'))
    return render_template('adminboard/editpage_id_category.html',
                           form=form, error=error
                           )
