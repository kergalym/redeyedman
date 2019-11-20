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
from application.core.dbmodel import Content
from application.core.dbmodel import Categories
from application.core.datalogics import SysInfo
from application.forms import contentpage_idform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from sqlalchemy import exc


@app.route('/adminboard/editpage_id_content/<int:id>', methods=['GET', 'POST'])
@login_required
def show_contentpageid(id):
    form = contentpage_idform.ContentpageidForm()
    editpage_output_loop = sql.session.query(Content).filter_by(id=id).first()
    categories_loop = sql.session.query(Categories).all()
    instance = SysInfo()
    atime = instance.altertime()
    author = g.user
    if (editpage_output_loop
            and categories_loop
            and atime
            and author is not None):
        return render_template(
            'adminboard/editpage_id_content.html',
            editpage_output_loop=editpage_output_loop,
            categories_loop=categories_loop,
            form=form)
    else:
        return redirect(url_for('show_login'))


@app.route('/adminboard/editpage_id_content/', methods=['GET', 'POST'])
@login_required
def update_contentpageid():
    error = None
    form = contentpage_idform.ContentpageidForm()
    instance = SysInfo()
    author = g.user

    if (request.method == 'POST' and author is not None
            and request.form['save']):
        if form.validate_on_submit():

            # we assign record time to this form element
            # as unicode string to be consistent with other form elements here
            form.content_date.data = unicode(instance.altertime())

            conn = engine.connect()
            stmt = update(Content).where(
                Content.id == form.id.data).values(
                id=form.id.data,
                content_title=form.content_title.data,
                content_author=form.content_author.data,
                content_category=form.content_category.data,
                content_date=form.content_date.data,
                content_text=form.content_text.data
            )

            try:
                conn.execute(stmt)
                flash("Content is changed", 'info')
            except exc.IntegrityError:
                flash("Content with same name is exist", 'error')
            return redirect(url_for('show_contentpageid',
                                    id=form.id.data))
    else:
        flash("Content is not changed", 'error')
        return redirect(url_for('show_contentpageid'))
    return render_template('adminboard/editpage_id_content.html',
                           form=form, error=error
                           )
