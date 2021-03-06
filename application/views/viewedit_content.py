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
from application.core.dbmodel import Content
from application.core.datalogics import SysInfo
from application.forms import contentpageform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from sqlalchemy import exc


@app.route('/adminboard/editpage_content/')
@login_required
def show_editpage_content():
    form = contentpageform.ContentpageAddForm()
    editpage_output_loop = Content.query.filter_by(
        content_author='admin'
    ).first()
    categories_loop = Categories.query.all()
    instance = SysInfo()
    atime = instance.altertime()
    author = g.user
    if (editpage_output_loop
            and categories_loop
            and atime
            and author is not None):
        return render_template(
            'adminboard/editpage_content.html',
            author=author, atime=atime,
            editpage_output_loop=editpage_output_loop,
            categories_loop=categories_loop,
            form=form)
    else:
        return redirect(url_for('show_login'))


@app.route('/adminboard/editpage_content/', methods=['GET', 'POST'])
@login_required
def add_editpage_content():
    form = contentpageform.ContentpageAddForm()
    author = g.user
    published = 0
    if (request.method == 'POST'
            and author is not None
            and form.validate_on_submit()):
        iid = request.form['id']
        content_title = request.form['content_title']
        content_author = request.form['content_author']
        content_category = request.form['content_category']
        content_date = request.form['content_date']
        content_text = request.form['content_text']
        contents = Content(iid, content_title, content_author,
                           content_category, content_date,
                           content_text, published)
        sql.session.add(contents)
        try:
            sql.session.commit()
            flash("Content {}: {} is added".format(iid, content_title), 'info')
        except exc.IntegrityError:
            flash("Content {}: {} is exist".format(iid, content_title), 'error')
        return redirect(url_for('show_dashboard_inner'))
    else:
        flash("Content text is empty", 'error')
        return redirect(url_for('show_dashboard_inner'))
    return render_template('adminboard/editpage_content.html',
                           form=form
                           )
