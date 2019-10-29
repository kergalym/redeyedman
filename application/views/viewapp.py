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
from application.core.dbmodel import Content
from application.forms import searchform
from application.core.datalogics import Paginator
from application.core.datalogics import Dlogics
from flask import request
from flask import render_template


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def show_index():
    per_page = 7
    search_limit = 4
    pages = request.args.get('page', type=int, default=1)
    form = searchform.SearchForm()
    articles = Articles.query.filter_by(article_author='admin').first()
    articles_loop = Articles.query.filter_by(article_category='Blender3D').all()
    contents = Content.query.filter_by(content_author='admin').all()
    c_howto = Articles.query.filter_by(article_category='HowTo').all()
    c_games = Articles.query.filter_by(article_category='Игры').all()
    c_misc = Articles.query.filter_by(article_category='разное').all()
    paginator = Paginator()
    dlogics = Dlogics()
    menu = sql.session.query(Articles).limit(
        (per_page)).offset(
        (pages - 1) * per_page).all()

    app.jinja_env.filters['ctxt'] = dlogics.textcutn

    pagination = paginator.paginate(Articles, pages, per_page)

    if request.method == 'POST' and form.validate_on_submit():

        s_menus = sql.session.query(Articles).filter(Articles.article_text.like(
            "%{}%".format(form.query.data))).limit(search_limit).offset(
            (pages - 1) * search_limit).all()

        return render_template('site/inner_search.html',
                               articles_loop=articles_loop, contents=contents,
                               c_howto=c_howto, c_games=c_games, c_misc=c_misc,
                               menus=menus, s_menus=s_menus,
                               pagination=pagination, form=form
                               )

    return render_template('site/index.html', articles=articles,
                           articles_loop=articles_loop, contents=contents,
                           c_howto=c_howto, c_games=c_games, c_misc=c_misc,
                           menu=menu, pagination=pagination, form=form
                           )


@app.route('/inner/', defaults={'id': 1})
@app.route('/inner/<int:id>', methods=['GET', 'POST'])
def show_inner(id):
    per_page = 7
    search_limit = 4
    pages = request.args.get('page', type=int, default=1)
    form = searchform.SearchForm()
    articles = Articles.query.filter_by(id=id).first()
    articles_loop = Articles.query.filter_by(article_category='Blender3D').all()
    contents = Content.query.filter_by(content_author='admin').all()
    c_howto = Articles.query.filter_by(article_category='HowTo').all()
    c_games = Articles.query.filter_by(article_category='Игры').all()
    c_misc = Articles.query.filter_by(article_category='разное').all()
    paginator = Paginator()
    dlogics = Dlogics()
    menus = sql.session.query(Articles).limit(
        (per_page)).offset(
        (pages - 1) * per_page).all()

    app.jinja_env.filters['ctxt'] = dlogics.textcutn

    pagination = paginator.paginate(Articles, pages, per_page)

    if request.method == 'POST' and form.validate_on_submit():

        s_menus = sql.session.query(Articles).filter(Articles.article_text.like(
            "%{}%".format(form.query.data))).limit(search_limit).offset(
            (pages - 1) * search_limit).all()

        return render_template('site/inner_search.html',
                               articles_loop=articles_loop, contents=contents,
                               c_howto=c_howto, c_games=c_games, c_misc=c_misc,
                               menus=menus, s_menus=s_menus,
                               pagination=pagination, form=form
                               )
    return render_template('site/inner.html', articles=articles,
                           articles_loop=articles_loop, contents=contents,
                           c_howto=c_howto, c_games=c_games, c_misc=c_misc,
                           menus=menus, pagination=pagination, form=form
                           )


@app.route('/inner_search/', methods=['GET', 'POST'])
def show_inner_search():
    per_page = 7
    search_limit = 4
    pages = request.args.get('page', type=int, default=1)
    form = searchform.SearchForm()
    articles_loop = Articles.query.filter_by(article_category='Blender3D').all()
    contents = Content.query.filter_by(content_author='admin').all()
    c_howto = Articles.query.filter_by(article_category='HowTo').all()
    c_games = Articles.query.filter_by(article_category='Игры').all()
    c_misc = Articles.query.filter_by(article_category='разное').all()
    paginator = Paginator()
    dlogics = Dlogics()
    menus = sql.session.query(Articles).limit(
        (per_page)).offset(
        (pages - 1) * per_page).all()

    app.jinja_env.filters['ctxt'] = dlogics.textcutn

    pagination = paginator.paginate(Articles, pages, per_page)

    if request.method == 'POST' and form.validate_on_submit():

        s_menus = sql.session.query(Articles).filter(Articles.article_text.like(
            "%{}%".format(form.query.data))).limit(search_limit).offset(
            (pages - 1) * search_limit).all()

        return render_template('site/inner_search.html',
                               articles_loop=articles_loop, contents=contents,
                               c_howto=c_howto, c_games=c_games, c_misc=c_misc,
                               menus=menus, s_menus=s_menus,
                               pagination=pagination, form=form
                               )
    else:
        s_menus = ''
        return render_template('site/inner_search.html',
                               articles_loop=articles_loop, contents=contents,
                               c_howto=c_howto, c_games=c_games, c_misc=c_misc,
                               menus=menus, s_menus=s_menus,
                               pagination=pagination, form=form
                               )
