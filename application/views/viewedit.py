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
from application.core.dbmodel import Articles
from application.core.datalogics import SysInfo
from application.forms import editpageform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from sqlalchemy import exc


@app.route('/adminboard/editpage/')
@login_required
def show_editpage():
    form = editpageform.EditpageAddForm()
    editpage_output_loop = Articles.query.filter_by(
        article_author='admin'
    ).first()
    categories_loop = Categories.query.all()
    instance = SysInfo()
    atime = instance.altertime()
    author = g.user
    if (editpage_output_loop and categories_loop
            and atime
            and author is not None):
        return render_template(
            'adminboard/editpage.html',
            author=author, atime=atime,
            editpage_output_loop=editpage_output_loop,
            categories_loop=categories_loop,
            form=form)
    else:
        return redirect(url_for('show_login'))


@app.route('/adminboard/editpage/', methods=['GET', 'POST'])
@login_required
def add_editpage():
    form = editpageform.EditpageAddForm()
    author = g.user
    published = 0
    if (request.method == 'POST'
            and author is not None
            and form.validate_on_submit()):
        iid = request.form['id']
        article_title = request.form['article_title']
        article_author = request.form['article_author']
        article_category = request.form['article_category']
        article_date = request.form['article_date']
        article_mod_date = request.form['article_date']
        article_text = request.form['article_text']
        articles = Articles(iid, article_title, article_author,
                            article_category, article_date,
                            article_mod_date, article_text,
                            published)
        sql.session.add(articles)
        try:
            sql.session.commit()
            flash("Article {}: {} is added".format(iid, article_title), 'info')
        except exc.IntegrityError:
            flash("Article {}: {} is exist".format(iid, article_title), 'error')
        return redirect(url_for('show_dashboard_main'))
    else:
        flash("Article text is empty", 'error')
        return redirect(url_for('show_dashboard_main'))

    return render_template('adminboard/editpage.html',
                           form=form
                           )
