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

import os
from werkzeug.utils import secure_filename
from application import app
from application import sql
from application import engine
from sqlalchemy import update
from sqlalchemy import delete
from application.core.dbmodel import Articles
from application.core.dbmodel import Categories
from application.core.dbmodel import Content
from application.core.dbmodel import Users
from application.core.datalogics import Base, Dlogics
from application.core.filemanagement import FileBrowser
from application.views.viewdash import ViewDash
from application.forms import dashboard_itemsform
from application.forms import dashboard_filesform
from application.forms import dashboard_searchform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from flask import g


class ViewUpdate(ViewDash):

    @app.route('/adminboard/adminboard_main/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_main(self):
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        dlogics = Dlogics()
        author = g.user
        items = []
        values = []
        conn = engine.connect()

        if request.method == 'POST' and request.form.get('rename', None) \
                and form.validate_on_submit():
            values = request.form
            items = request.form.getlist('item_chb')
            if author is not None:
                stmt = update(Articles).where(
                    Articles.id == request.form['item_chb']
                ).values(
                    id=request.form['delid_' + request.form['item_chb']]
                )
                conn.execute(stmt)
                flash("Item is updated!", 'info')
                return redirect(url_for('show_dashboard_main'))
            elif author is not None:
                mixed = items, values[:-2]
                for index in mixed:
                    stmt = update(Articles).where(
                        Articles.id == index[0]
                    ).values(
                        id=index[1]
                    )
                    conn.execute(stmt)
                flash("Items is updated!", 'info')
                return redirect(url_for('show_dashboard_main'))
        elif request.method == 'POST' and request.form.get('delete', None) \
                and form.validate_on_submit():
            items = request.form.getlist('items_chb')
            stmt = delete(Articles).where(
                Articles.id == request.form['item_chb'])
            conn.execute(stmt)
            flash("Item is deleted!", 'info')
            return redirect(url_for('show_dashboard_main'))
        elif request.method == 'POST' and form_next.validate_on_submit():
            data = []
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
            flash("Items are not updated or deleted!", 'error')
            return redirect(url_for('show_dashboard_main'))
        return render_template('adminboard/adminboard_main.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_inner/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_inner(self):
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        items = []
        values = []
        conn = engine.connect()
        if request.method == 'POST' and request.form.get('rename', None) \
                and form.validate_on_submit():
            values = request.form
            items = request.form.getlist('item_chb')
            if author is not None:
                stmt = update(Content).where(
                    Content.id == request.form['item_chb']
                ).values(
                    id=request.form['delid_' + request.form['item_chb']]
                )
                conn.execute(stmt)
                flash("Item is updated!", 'info')
                return redirect(url_for('show_dashboard_inner'))
            elif author is not None:
                mixed = items, values[:-2]
                for index in mixed:
                    stmt = update(Content).where(
                        Content.id == index[0]
                    ).values(
                        id=index[1]
                    )
                    conn.execute(stmt)
                flash("Items is updated!", 'info')
                return redirect(url_for('show_dashboard_inner'))
        elif request.method == 'POST' and request.form.get('delete', None) \
                and form.validate_on_submit():
            items = request.form.getlist('items_chb')
            stmt = delete(Content).where(
                Content.id == request.form['item_chb'])
            conn.execute(stmt)
            flash("Item is deleted!", 'info')
            return redirect(url_for('show_dashboard_inner'))
        elif request.method == 'POST' and form_next.validate_on_submit():
            data = []
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
            flash("Items are not updated or deleted!", 'error')
            return redirect(url_for('show_dashboard_inner'))
        return render_template('adminboard/adminboard_inner.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_category/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_category(self):
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        items = []
        values = []
        conn = engine.connect()
        if request.method == 'POST' and request.form.get('rename', None) \
                and form.validate_on_submit():
            values = request.form
            items = request.form.getlist('item_chb')
            if author is not None:
                stmt = update(Categories).where(
                    Categories.id == request.form['item_chb']
                ).values(
                    id=request.form['delid_' + request.form['item_chb']]
                )
                conn.execute(stmt)
                flash("Item is updated!", 'info')
                return redirect(url_for('show_dashboard_category'))
            elif author is not None:
                mixed = items, values[:-2]
                for index in mixed:
                    stmt = update(Categories).where(
                        Categories.id == index[0]
                    ).values(
                        id=index[1]
                    )
                    conn.execute(stmt)
                flash("Items is updated!", 'info')
                return redirect(url_for('show_dashboard_category'))
        elif request.method == 'POST' and request.form.get('delete', None) \
                and form.validate_on_submit():
            items = request.form.getlist('items_chb')
            stmt = delete(Categories).where(
                Categories.id == request.form['item_chb'])
            conn.execute(stmt)
            flash("Item is deleted!", 'info')
            return redirect(url_for('show_dashboard_category'))
        elif request.method == 'POST' and form_next.validate_on_submit():
            data = []
            data_array = sql.session.query(Categories).filter(
                Categories.category_title.match(request.form['query']
                                                )).all()
            for x in data_array:
                data = x

            return jsonify(id=str(data.id),
                           title=data.category_title,
                           date=data.category_date
                           )
        else:
            flash("Items are not updated or deleted!", 'error')
            return redirect(url_for('show_dashboard_category'))
        return render_template('adminboard/adminboard_category.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_users/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_users(self):
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        items = []
        values = []
        conn = engine.connect()
        if request.method == 'POST' and request.form.get('rename', None) \
                and form.validate_on_submit():
            values = request.form
            items = request.form.getlist('item_chb')
            if author is not None:
                conn = engine.connect()
                stmt = update(Users).where(
                    Users.id == request.form['item_chb']
                ).values(
                    id=request.form['delid_' + request.form['item_chb']]
                )
                conn.execute(stmt)
                flash("Item is updated!", 'info')
                return redirect(url_for('show_dashboard_users'))
            elif author is not None:
                mixed = items, values[:-2]
                for index in mixed:
                    stmt = update(Users).where(
                        Users.id == index[0]
                    ).values(
                        id=index[1]
                    )
                    conn.execute(stmt)
                flash("Items is updated!", 'info')
                return redirect(url_for('show_dashboard_users'))
        elif request.method == 'POST' and request.form.get('delete', None) \
                and form.validate_on_submit():
            items = request.form.getlist('items_chb')
            stmt = delete(Users).where(
                Users.id == request.form['item_chb'])
            conn.execute(stmt)
            flash("Item is deleted!", 'info')
            return redirect(url_for('show_dashboard_users'))
        elif request.method == 'POST' and form_next.validate_on_submit():
            data = []
            data_array = sql.session.query(Users).filter(
                Users.login.match(request.form['query']
                                  )).all()
            for x in data_array:
                data = x

            return jsonify(id=str(data.id),
                           login=data.login,
                           email=data.email,
                           date=data.regdate
                           )
        else:
            flash("Items are not updated or deleted!", 'error')
            return redirect(url_for('show_dashboard_users'))
        return render_template('adminboard/adminboard_users.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_media/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_media(self):
        form = dashboard_filesform.DashboardFilesForm()
        fileserving = FileBrowser()
        if request.method == 'POST' \
                and form.validate_on_submit() \
                and form_media.validate_on_submit():
            if request.form['f-upload']:
                file = request.files['file']
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)

                if file and fileserving.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                           filename))
                    return redirect(url_for('uploaded_file',
                                            filename=filename))

            if request.form['cddir']:
                get_path = form.cddir.data
                fileserving.show_files(get_path)
                return redirect(url_for('show_dashboard_media'))

            if request.form['delete']:
                get_object = os.path + "/static" \
                             + request.form['delid_' + request.form['item_chb']]
                fileserving.del_file_dir(get_object)
                return redirect(url_for('show_dashboard_media'))

            if request.form['rename']:
                old_object = os.path + "/static" \
                             + request.form['item_chb']
                new_object = os.path + "/static" \
                             + request.form['delid_' + request.form['item_chb']]
                if fileserving.rename_file_dir(
                        old_object,
                        new_object) != 'Not str':
                    return fileserving.rename_file_dir(old_object, new_object)
                    return redirect(url_for('show_dashboard_media'))
                else:
                    flash(old_object + " is not renamed to " \
                          + new_object, 'error')
                    return redirect(url_for('show_dashboard_media'))
            else:
                flash("No button is pressed", 'error')
                return redirect(url_for('show_dashboard_media'))

            if request.form['mkdir']:
                get_dirname = form.cdir.data
                fileserving.make_dir(get_dirname)
                return redirect(url_for('show_dashboard_media'))
        else:
            flash("Items are not processed!", 'error')
            return redirect(url_for('show_dashboard_media'))

            return render_template('adminboard/adminboard_media.html',
                                   form=form
                                   )

    @app.route('/adminboard/adminboard_settings/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_settings():
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        items = []
        values = []
        conn = engine.connect()
        if request.method == 'POST' and request.form.get('rename', None) \
                and form.validate_on_submit():
            values = request.form
            items = request.form.getlist('item_chb')
            if author is not None:
                conn = engine.connect()
                stmt = update(Users).where(
                    Users.id == request.form['item_chb']
                ).values(
                    id=request.form['delid_' + request.form['item_chb']]
                )
                conn.execute(stmt)
                flash("Item is updated!", 'info')
                return redirect(url_for('show_dashboard_settings'))
            elif author is not None:
                mixed = items, values[:-2]
                for index in mixed:
                    stmt = update(Users).where(
                        Users.id == index[0]
                    ).values(
                        id=index[1]
                    )
                    conn.execute(stmt)
                flash("Items is updated!", 'info')
                return redirect(url_for('show_dashboard_settings'))
        elif request.method == 'POST' and request.form.get('delete', None) \
                and form.validate_on_submit():
            items = request.form.getlist('items_chb')
            stmt = delete(Users).where(
                Users.id == request.form['item_chb'])
            conn.execute(stmt)
            flash("Item is deleted!", 'info')
            return redirect(url_for('show_dashboard_settings'))
        elif request.method == 'POST' and form_next.validate_on_submit():
            data = []
            data_array = sql.session.query(Users).filter(
                Users.login.match(request.form['query']
                                  )).all()
            for x in data_array:
                data = x

            return jsonify(id=str(data.id),
                           login=data.login,
                           email=data.email,
                           date=data.regdate
                           )
        else:
            flash("Items are not updated or deleted!", 'error')
            return redirect(url_for('show_dashboard_settings'))
        return render_template('adminboard/adminboard_settings.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_filemanager/', methods=['GET', 'POST'])
    def upload_file(self):
        fileserving = FileBrowser()
        if request.method == 'POST' and form.validate_on_submit():
            if request.form['delete']:
                get_object = os.path + "/static" \
                             + request.form['delid_' + request.form['item_chb']]
                fileserving.del_file_dir(get_object)

            if request.form['rename']:
                old_object = os.path + "/static" \
                             + request.form['item_chb']
                new_object = os.path + "/static" \
                             + request.form['delid_' + request.form['item_chb']]
                if fileserving.rename_file_dir(
                        old_object,
                        new_object) != 'Not str':
                    return fileserving.rename_file_dir(old_object, new_object)
                else:
                    flash(old_object + " is not renamed to " \
                          + new_object, 'error')
            else:
                flash("No button is pressed", 'error')

            if request.form['cdir']:
                get_dirname = form.cdir.data
                fileserving.make_dir(get_dirname)

            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and fileserving.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploaded_file',
                                        filename=filename))

        return render_template('adminboard/adminboard_filemanager.html',
                               form=form
                               )
