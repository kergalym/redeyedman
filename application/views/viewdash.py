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
from os import remove
from os.path import exists, isfile

from application import app
from application import sql
from application import session
from application import session_timein
from application import bcrypt
from application import login_manager
from application.core.dbmodel import Articles
from application.core.dbmodel import Categories
from application.core.dbmodel import Content
from application.core.dbmodel import Users
from application.core.datalogics import SysInfo
from application.core.datalogics import Base, Paginator
from application.core.filemanagement import FileBrowser
from application.forms import loginform
from application.forms import dashboard_itemsform
from application.forms import dashboard_filesform
from flask import session as session
from flask import flash
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import current_app
from flask import g
from flask import url_for
from flask_login import current_user
from flask_user import roles_required
from flask_login import login_user
from flask_login import logout_user
from functools import wraps
import socket
import os


class ViewDash:

    @app.route('/login/', methods=['GET', 'POST'])
    def show_login():
        form = loginform.LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            user = sql.session.query(Users).filter_by(
                login=form.login.data
            ).first()
            if user is not None and \
                bcrypt.check_password_hash(
                    user.password,
                    form.password.data):
                session['SECRET_KEY'] = True
                session['login'] = user.login
                login_user(user)
                return redirect(url_for('show_dashboard'))
            else:
                flash('Invalid login or password.', 'error')
        return render_template('adminboard/login.html', form=form)

    login_manager.login_view = 'show_login'

    @app.before_request
    def load_user():
        g.user = None
        user = None
        if 'login' in session:
            user = sql.session.query(Users).filter_by(
                login=session["login"]).first()
            g.user = user.login

        session.permanent = True

        if session_timein == 0:
            session.clear()
            return redirect(url_for('show_login', next=request.url))

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user is None:
                return redirect(url_for('show_login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/logout/')
    @login_required
    def user_logout():
        logout_user()
        session.clear()
        if (exists(("{}/static/get_path.tmp".format(app.root_path)))
                and isfile(("{}/static/get_path.tmp".format(app.root_path)))):
            remove("{}/static/get_path.tmp".format(app.root_path))
        return redirect(url_for('show_login'))

    @app.route('/adminboard/')
    @login_required
    def show_dashboard():
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        else:
            servername = socket.gethostname()
            approot = os.path.split(app.root_path)
            users = g.user
            instance = SysInfo()
            freespace = instance.diskspace()
            ltime = instance.systime()
            atime = instance.altertime()
            flash('Welcome, ' + users, 'info')
            return render_template('adminboard/adminboard.html',
                                   servername=servername, approot=approot[-2],
                                   freespace=freespace, users=users, ltime=ltime,
                                   atime=atime
                                   )

    @app.route('/adminboard/adminboard_main/')
    @login_required
    def show_dashboard_main():
        per_page = 9
        pages = request.args.get('page', type=int, default=1)
        paginator = Paginator()
        form = dashboard_itemsform.DashboardItemsForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        if not users and pages is None:
            abort(404)
        else:
            articles_loop = sql.session.query(Articles).limit(
                per_page).offset(
                (pages - 1) * per_page).all()
            pagination = paginator.paginate(Articles, pages, per_page)
            return render_template('adminboard/adminboard_main.html',
                                   servername=servername,
                                   approot=approot[-2],
                                   freespace=freespace,
                                   users=users, ltime=ltime,
                                   atime=atime,
                                   articles_loop=articles_loop,
                                   form=form,
                                   pagination=pagination
                                   )

    @app.route('/adminboard/adminboard_inner/')
    @login_required
    def show_dashboard_inner():
        per_page = 9
        paginator = Paginator()
        form = dashboard_itemsform.DashboardItemsForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        pages = request.args.get('page', type=int, default=1)
        if not users and pages == None:
            abort(404)
        else:
            contents_loop = sql.session.query(Content).limit(
                (per_page)).offset(
                (pages - 1) * per_page).all()
            pagination = paginator.paginate(Content, pages, per_page)
            return render_template('adminboard/adminboard_inner.html',
                                   servername=servername,
                                   approot=approot[-2],
                                   freespace=freespace,
                                   users=users, ltime=ltime,
                                   atime=atime,
                                   contents_loop=contents_loop,
                                   form=form,
                                   pagination=pagination
                                   )

    @app.route('/adminboard/adminboard_category/')
    @login_required
    def show_dashboard_category():
        per_page = 9
        paginator = Paginator()
        categories_loop = []
        form = dashboard_itemsform.DashboardItemsForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        pages = request.args.get('page', type=int, default=1)
        if not users and pages is None:
            abort(404)
        else:
            categories_loop = sql.session.query(Categories).limit(
                (per_page)).offset(
                (pages - 1) * per_page).all()

            pagination = paginator.paginate(Categories, pages, per_page)
            return render_template('adminboard/adminboard_category.html',
                                   servername=servername,
                                   approot=approot[-2],
                                   freespace=freespace,
                                   users=users, ltime=ltime,
                                   atime=atime,
                                   categories_loop=categories_loop,
                                   form=form,
                                   pagination=pagination
                                   )

    @app.route('/adminboard/adminboard_users/')
    @login_required
    # TODO: user privilegies
    def show_dashboard_users():
        per_page = 9
        paginator = Paginator()
        form = dashboard_itemsform.DashboardItemsForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        pages = request.args.get('page', type=int, default=1)
        if not users and pages is None:
            abort(404)
        else:
            users_loop = sql.session.query(Users).limit(
                (per_page)).offset(
                (pages - 1) * per_page).all()

            pagination = paginator.paginate(Users, pages, per_page)
            return render_template('adminboard/adminboard_users.html',
                                   servername=servername,
                                   approot=approot[-2],
                                   freespace=freespace,
                                   users=users, ltime=ltime,
                                   atime=atime,
                                   users_loop=users_loop,
                                   form=form,
                                   pagination=pagination
                                   )

    @app.route('/adminboard/adminboard_settings/')
    @login_required
    # TODO: user privilegies
    #@roles_required('admin')
    def show_dashboard_settings():
        per_page = 9
        paginator = Paginator()
        users_loop = []
        form = dashboard_itemsform.DashboardItemsForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        pages = request.args.get('page', type=int, default=1)

        if session['login'] != 'admin':
            flash("You don't have administrator privilegies!", 'error')
            return redirect(url_for('show_dashboard'))

        if not users and pages == None:
            abort(404)
        else:
            users_loop = sql.session.query(Users).limit(
                (per_page)).offset(
                (pages - 1) * per_page).all()

            pagination = paginator.paginate(Users, pages, per_page)
            return render_template('adminboard/adminboard_settings.html',
                                   servername=servername,
                                   approot=approot[-2],
                                   freespace=freespace,
                                   users=users, ltime=ltime,
                                   atime=atime,
                                   users_loop=users_loop,
                                   form=form,
                                   pagination=pagination
                                   )

    @app.route('/adminboard/adminboard_media/')
    @login_required
    # TODO: user privilegies
    # @roles_required('admin')
    def show_dashboard_media():
        browser = FileBrowser()
        per_page = 9
        pages = request.args.get('page', type=int, default=1)
        paginator = Paginator()
        form = dashboard_filesform.DashboardFilesForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        f = None
        get_relpath = None

        if session['login'] != 'admin':
            flash("You don't have administrator privilegies!", 'error')
            return redirect(url_for('show_dashboard'))

        if not users and pages is None:
            abort(404)
        else:

            if exists("{}/static/get_path.tmp".format(app.root_path)) is False:
                get_relpath = "/static/images/"
            elif exists("{}/static/get_path.tmp".format(app.root_path)):
                with open("{}/static/get_path.tmp".format(app.root_path), 'r') as f:
                    get_relpath = f.read()

            limit = per_page

            if get_relpath == '':
                get_relpath = "/static/images/"

            files = browser.show_files(get_relpath)
            offset = ((pages - 1) * per_page)
            if pages == 0 or pages == 1:
                f = files[:limit]
            elif len(files)-offset > offset:
                f = files[offset:-offset]
            elif len(files)-offset < offset:
                f = files[offset:]
            pagination = paginator.paginate(files, pages, per_page)
            return render_template('adminboard/adminboard_media.html',
                                   servername=servername,
                                   approot=approot[-2],
                                   freespace=freespace,
                                   users=users, ltime=ltime,
                                   atime=atime,
                                   files=f,
                                   get_relpath=get_relpath,
                                   form=form,
                                   pagination=pagination
                                   )

    @app.route('/adminboard/adminboard_filemanager/')
    @login_required
    # TODO: user privilegies
    # @roles_required('admin')
    def show_dashboard_filenamanager():
        browser = FileBrowser()
        per_page = 9
        pages = request.args.get('page', type=int, default=1)
        paginator = Paginator()
        form = dashboard_filesform.DashboardFilesForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        f = None
        get_relpath = None

        if session['login'] != 'admin':
            flash("You don't have administrator privilegies!", 'error')
            return redirect(url_for('show_dashboard'))

        if not users and pages is None:
            abort(404)
        else:

            if exists("{}/static/get_path.tmp".format(app.root_path)) is False:
                get_relpath = "/static/images/"
            elif exists("{}/static/get_path.tmp".format(app.root_path)):
                with open("{}/static/get_path.tmp".format(app.root_path), 'r') as f:
                    get_relpath = f.read()

            limit = per_page

            if get_relpath == '':
                get_relpath = "/static/images/"

            files = browser.show_files(get_relpath)
            offset = ((pages - 1) * per_page)
            if pages == 0 or pages == 1:
                f = files[:limit]
            elif len(files)-offset > offset:
                f = files[offset:-offset]
            elif len(files)-offset < offset:
                f = files[offset:]
            pagination = paginator.paginate(files, pages, per_page)
            return render_template('adminboard/adminboard_filemanager.html',
                                   servername=servername,
                                   approot=approot[-2],
                                   freespace=freespace,
                                   users=users, ltime=ltime,
                                   atime=atime,
                                   files=f,
                                   get_relpath=get_relpath,
                                   form=form,
                                   pagination=pagination
                                   )
