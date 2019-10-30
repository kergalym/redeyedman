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
from application.core.dbmodel import Articles
from application.core.dbmodel import Categories
from application.core.dbmodel import Content
from application.core.dbmodel import Users
from application.forms import dashboard_searchform
from flask_login import login_required
from flask import redirect
from flask import request
from flask import url_for
from flask import jsonify


@app.route('/adminboard/adminboard_main/', methods=['POST'])
@login_required
def search_dasboard_main():

    data = []
    form = dashboard_searchform.DashboardSearchForm()

    if request.method == 'POST' and form.validate_on_submit():

        data_array = sql.session.query(Articles).filter(
            Articles.article_title.match(request.form['query']
                                         )).all()
        for x in data_array:
            data = x

        return jsonify(id=str(data.id),
                       title=data.article_title,
                       author=data.article_author,
                       category=data.article_category,
                       date=data.article_date
                       )
    else:
        return redirect(url_for('show_dashboard_main'))


@app.route('/adminboard/adminboard_category/', methods=['POST'])
@login_required
def search_dasboard_category():

    data = []
    form = dashboard_searchform.DashboardSearchForm()

    if request.method == 'POST' and form.validate_on_submit():
        if request.form['query'] is not None:
            data_array = sql.session.query(Categories).filter(
                Categories.category_title.match(request.form['query']
                                                )).all()
            for x in data_array:
                data = x

            return jsonify(id=str(data.id),
                           title=data.category_title,
                           author=data.category_author,
                           category=data.category_category,
                           date=data.category_date
                           )


@app.route('/adminboard/adminboard_inner/', methods=['POST'])
@login_required
def search_dasboard_inner():

    data = []
    form = dashboard_searchform.DashboardSearchForm()

    if request.method == 'POST' and form.validate_on_submit():

        data_array = sql.session.query(Content).filter(
            Content.content_title.match(request.form['query']
                                        )).all()
        for x in data_array:
            data = x

        return jsonify(id=str(data.id),
                       title=data.content_title,
                       author=data.content_author,
                       category=data.content_category,
                       date=data.content_date
                       )
    else:
        return False


@app.route('/adminboard/adminboard_users/', methods=['POST'])
@login_required
def search_dasboard_users():

    data = []
    form = dashboard_searchform.DashboardSearchForm()

    if request.method == 'POST' and form.validate_on_submit():

        data_array = sql.session.query(Users).filter(
            Users.login.match(request.form['query']
                              )).all()
        for x in data_array:
            data = x.login
            data = x.email
            data = x.regdate
            data = x.usr_level

        return jsonify(id=str(data.id),
                       title=data.login,
                       author=data.regdate,
                       date=data.regdate
                       )
    else:
        return False
