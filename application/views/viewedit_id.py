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
from application.core.dbmodel import Articles
from application.core.dbmodel import Categories
from application.core.datalogics import SysInfo
from application.forms import editpage_idform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g


class ViewEdit:
    #
    #   ARTICLES EDITPAGE ADD
    #

    @app.route('/adminboard/editpage_id/<int:id>', methods=['GET', 'POST'])
    @login_required
    def show_editpageid(id):
        form = editpage_idform.EditpageidForm()
        editpage_output_loop = sql.session.query(Articles).filter_by(id=id).first()
        categories_loop = sql.session.query(Categories).all()
        instance = SysInfo()
        atime = instance.altertime() 
        author = g.user
        if editpage_output_loop and categories_loop \
            and atime and author is not None:
            return render_template(
                                    'adminboard/editpage_id.html', 
                                    editpage_output_loop=editpage_output_loop,
                                    categories_loop=categories_loop,
                                    form=form)
        else:
            return redirect(url_for('show_login'))


    @app.route('/adminboard/editpage_id/', methods=['GET', 'POST'])
    @login_required
    def update_editpageid():
        error = None
        form = editpage_idform.EditpageidForm()
        instance = SysInfo()
        atime = instance.altertime()
        author = g.user
        if request.method == 'POST' and author is not None \
            and request.form['save']:
            if form.validate_on_submit():
                conn = engine.connect()
                stmt = update(Articles).where(
                Articles.id==form.id.data).values(
                id=form.id.data,
                article_title=form.article_title.data,
                article_author=form.article_author.data,
                article_category=form.article_category.data,
                article_date=atime,
                article_text=form.article_text.data
                )
                conn.execute(stmt)
                error = "Article is changed"
                return redirect(url_for('show_editpageid', 
                                        id=form.id.data))
        else:
            error = "Article is not changed"
            return redirect(url_for('show_dashboard_main'))
        return render_template('adminboard/editpage_id.html',
                                form=form, error=error
                                ) 
                       