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

import re
from os.path import exists, isdir

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
from application.core.filemanagement import FileBrowser
from application.views.viewdash import ViewDash
from application.forms import dashboard_itemsform
from application.forms import dashboard_filesform
from application.forms import dashboard_searchform
from flask_login import login_required
from flask import send_from_directory
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
    def update_dashboard_main():
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        conn = engine.connect()

        if request.method == 'POST':
            if form.rename.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                # form.delid.data is the unicode list thing which
                # we convert to integer using regexp
                delid = int(re.search("\d+", str(form.delid.data)).group())

                if author is not None:
                    articles = Articles.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n and x != delid:
                            stmt = update(Articles).where(
                                Articles.id == x
                            ).values(
                                id=delid
                            )
                            conn.execute(stmt)
                            flash("Item {} is changed to {}".format(x,
                                                                    form.delid.data), 'info')
                        elif x == delid:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not changed to {}".format(x,
                                                                        form.delid.data), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_main'))

            elif form.rename.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_main'))

            elif form.delete.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                if author is not None:
                    articles = Articles.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n:
                            stmt = delete(Articles).where(
                                Articles.id == x)
                            conn.execute(stmt)
                            flash("Item {} is deleted!".format(x), 'info')
                        elif x == n:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not deleted!".format(x), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_main'))

            elif form.delete.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_main'))

            elif form_next.validate_on_submit():
                data = []
                data_array = sql.session.query(Articles).filter(
                    Articles.article_title.match(form.query.data)).all()
                for x in data_array:
                    data = x

                return jsonify(id=str(data.id),
                               title=data.article_title,
                               author=data.article_author,
                               category=data.article_category,
                               date=data.article_date
                               )

        return render_template('adminboard/adminboard_main.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_inner/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_inner():
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        conn = engine.connect()

        if request.method == 'POST':
            if form.rename.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                # form.delid.data is the unicode list thing which
                # we convert to integer using regexp
                delid = int(re.search("\d+", str(form.delid.data)).group())

                if author is not None:
                    articles = Content.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n and x != delid:
                            stmt = update(Content).where(
                                Content.id == x
                            ).values(
                                id=delid
                            )
                            conn.execute(stmt)
                            flash("Item {} is changed to {}".format(x,
                                                                    form.delid.data), 'info')
                        elif x == delid:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not changed to {}".format(x,
                                                                        form.delid.data), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_inner'))

            elif form.rename.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_inner'))

            elif form.delete.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                if author is not None:
                    articles = Content.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n:
                            stmt = delete(Content).where(
                                Content.id == x)
                            conn.execute(stmt)
                            flash("Item {} is deleted!".format(x), 'info')
                        elif x == n:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not deleted!".format(x), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_inner'))

            elif form.delete.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_inner'))
            elif form_next.validate_on_submit():
                data = []
                data_array = sql.session.query(Content).filter(
                    Content.content_title.match(form.query.data)).all()
                for x in data_array:
                    data = x

                return jsonify(id=str(data.id),
                               title=data.content_title,
                               author=data.content_author,
                               category=data.content_category,
                               date=data.content_date
                               )

        return render_template('adminboard/adminboard_inner.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_category/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_category():
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        conn = engine.connect()

        if request.method == 'POST':
            if form.rename.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                # form.delid.data is the unicode list thing which
                # we convert to integer using regexp
                delid = int(re.search("\d+", str(form.delid.data)).group())

                if author is not None:
                    articles = Categories.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n and x != delid:
                            stmt = update(Categories).where(
                                Categories.id == x
                            ).values(
                                id=delid
                            )
                            conn.execute(stmt)
                            flash("Item {} is changed to {}".format(x,
                                                                    form.delid.data), 'info')
                        elif x == delid:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not changed to {}".format(x,
                                                                        form.delid.data), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_category'))

            elif form.rename.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_category'))

            elif form.delete.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                if author is not None:
                    articles = Categories.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n:
                            stmt = delete(Categories).where(
                                Categories.id == x)
                            conn.execute(stmt)
                            flash("Item {} is deleted!".format(x), 'info')
                        elif x == n:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not deleted!".format(x), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_category'))

            elif form.delete.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_category'))

            elif form_next.validate_on_submit():
                data = []
                data_array = sql.session.query(Categories).filter(
                    Categories.category_title.match(form.query.data)).all()
                for x in data_array:
                    data = x

                return jsonify(id=str(data.id),
                               title=data.category_title,
                               date=data.category_date
                               )

        return render_template('adminboard/adminboard_category.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_users/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_users():
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        conn = engine.connect()

        if request.method == 'POST':
            if form.rename.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                # form.delid.data is the unicode list thing which
                # we convert to integer using regexp
                delid = int(re.search("\d+", str(form.delid.data)).group())

                if author is not None:
                    articles = Users.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n and x != delid:
                            stmt = update(Users).where(
                                Users.id == x
                            ).values(
                                id=delid
                            )
                            conn.execute(stmt)
                            flash("Item {} is changed to {}".format(x,
                                                                    form.delid.data), 'info')
                        elif x == delid:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not changed to {}".format(x,
                                                                        form.delid.data), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_users'))

            elif form.rename.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_users'))

            elif form.delete.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                if author is not None:
                    articles = Users.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n:
                            stmt = delete(Users).where(
                                Users.id == x)
                            conn.execute(stmt)
                            flash("Item {} is deleted!".format(x), 'info')
                        elif x == n:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not deleted!".format(x), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_users'))

            elif form.delete.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_users'))

        elif form_next.validate_on_submit():
            data = []
            data_array = sql.session.query(Users).filter(
                Users.login.match(form.query.data)).all()
            for x in data_array:
                data = x

            return jsonify(id=str(data.id),
                           login=data.login,
                           email=data.email,
                           date=data.regdate
                           )

        return render_template('adminboard/adminboard_users.html',
                               form=form
                               )

    @app.route('/application/static/images/<filename>')
    def upldd_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)

    @app.route('/adminboard/adminboard_media/', methods=['GET', 'POST'])
    @login_required
    # TODO: add arg self to the decorator
    def update_dashboard_media():
        form_mkdir = dashboard_filesform.DashboardMkdirForm()
        form_cddir = dashboard_filesform.DashboardCddirForm()
        form_upload = dashboard_filesform.DashboardUploadForm()
        form_files = dashboard_filesform.DashboardFilesForm()
        fileserving = FileBrowser()

        if request.method == 'POST':
            file = request.files['f_upload']

            # when working in upload context check if unwanted buttons are not pressed
            if (file.filename == ''
                    and form_cddir.cddir.data is False
                    and form_mkdir.mkdir.data is False
                    and form_files.rename.data is False
                    and form_files.delete.data is False
                    and form_upload.validate_on_submit()):
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            # check if the post request has the file part
            elif 'f_upload' not in request.files:
                flash('No file part')
                return redirect(request.url)

            # when working in upload context check if unwanted buttons are not pressed
            elif (file.filename
                  and form_cddir.cddir.data is False
                  and form_mkdir.mkdir.data is False
                  and form_files.rename.data is False
                  and form_files.delete.data is False
                  and form_upload.validate_on_submit()):

                # when working in upload context check if unwanted buttons are not pressed
                if (file.filename
                        and form_cddir.cddir.data is False
                        and form_mkdir.mkdir.data is False
                        and form_files.rename.data is False
                        and form_files.delete.data is False
                        and fileserving.allowed_file(file.filename)
                        and exists("{}{}".format(app.root_path,
                                                 request.form['addressbar']))):
                    filename = secure_filename(file.filename)
                    fpath = "{}{}{}".format(app.root_path, request.form['addressbar'], filename)
                    if filename and exists(fpath) is False:
                        file.save(fpath)
                        flash("{}{} is uploaded".format(request.form['addressbar'], filename), 'info')
                    elif exists(fpath):
                        flash("{}{} is exists".format(request.form['addressbar'], filename), 'error')
                    else:
                        flash("{}{} is not uploaded".format(request.form['addressbar'], filename), 'error')

                return redirect(url_for('show_dashboard_media'))

            elif (form_cddir.cddir.data
                  and form_cddir.validate_on_submit()):

                get_path = str(form_cddir.addressbar.data)

                if (exists("{}{}".format(app.root_path, get_path))
                        and isdir("{}{}".format(app.root_path, get_path))):

                    with open("{}/static/get_path.tmp".format(app.root_path), 'w') as f:
                        f.write(get_path)

                    fileserving.show_files(get_path)
                    flash("Location is changed to {} ".format(get_path), 'info')
                else:
                    flash("Location is not changed to {} ".format(get_path), 'error')
                return redirect(url_for('show_dashboard_media'))

            elif form_cddir.cddir.data is True and form_cddir.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            elif (form_mkdir.mkdir.data
                  and form_mkdir.validate_on_submit()):

                get_root_dirname = "{}{}".format(app.root_path, form_mkdir.addressbar.data)
                newdirname = form_mkdir.newdirname.data

                if exists(get_root_dirname) is True:
                    if exists("{}{}".format(get_root_dirname, newdirname)) is False and newdirname is not None:
                        fileserving.make_dir("{}{}".format(get_root_dirname, newdirname))
                        flash("Directory {}{} is created".format(get_root_dirname, newdirname), 'info')
                    elif exists("{}{}".format(get_root_dirname, newdirname)) is True and newdirname is not None:
                        flash("Directory {}{} is exists".format(get_root_dirname, newdirname), 'error')
                else:
                    flash("Directory {} is not exist. Please check the path".format(get_root_dirname), 'error')
                return redirect(url_for('show_dashboard_media'))

            elif form_mkdir.mkdir.data is True and form_mkdir.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            elif (form_files.rename.data
                  and form_files.validate_on_submit()):

                if (len(request.form.getlist('item_chb')) == 1
                        and len(request.form.getlist('delid')) == 1
                        and isinstance(request.form['addressbar'], unicode)):
                    old_object = "{}{}{}".format(app.root_path,
                                                 request.form['addressbar'],
                                                 request.form.get('item_chb'))
                    new_object = "{}{}{}".format(app.root_path,
                                                 request.form['addressbar'],
                                                 form_files.delid.data)

                    if exists(old_object):
                        fileserving.rename_file_dir(old_object, new_object)
                        flash("{} is renamed to {}".format(old_object,
                                                           new_object), 'info')
                    else:
                        flash("{} is not renamed to {}".format(old_object,
                                                               new_object), 'error')
                return redirect(url_for('show_dashboard_media'))

            elif form_files.rename.data is True and form_files.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            elif (form_files.delete.data
                  and form_files.validate_on_submit()):

                if (len(request.form.getlist('item_chb')) == 1
                        and isinstance(request.form['addressbar'], unicode)):
                    get_object = "{}{}{}".format(app.root_path,
                                                 request.form['addressbar'],
                                                 request.form['item_chb'])
                    if exists(get_object):
                        fileserving.del_file_dir(get_object)
                        flash("{} is deleted".format(get_object), 'info')
                    else:
                        flash("{} was not deleted".format(get_object), 'error')
                    return redirect(url_for('show_dashboard_media'))

            elif form_files.delete.data is True and form_files.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            return render_template('adminboard/adminboard_media.html',
                                   form=form_mkdir
                                   )
        return render_template('adminboard/adminboard_media.html',
                               form=form_mkdir
                               )

    @app.route('/adminboard/adminboard_settings/', methods=['GET', 'POST'])
    @login_required
    def update_dashboard_settings():
        form = dashboard_itemsform.DashboardItemsForm()
        form_next = dashboard_searchform.DashboardSearchForm()
        author = g.user
        conn = engine.connect()

        if request.method == 'POST':
            if form.rename.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                # form.delid.data is the unicode list thing which
                # we convert to integer using regexp
                delid = int(re.search("\d+", str(form.delid.data)).group())

                if author is not None:
                    articles = Users.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n and x != delid:
                            stmt = update(Users).where(
                                Users.id == x
                            ).values(
                                id=delid
                            )
                            conn.execute(stmt)
                            flash("Item {} is changed to {}".format(x,
                                                                    form.delid.data), 'info')
                        elif x == delid:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not changed to {}".format(x,
                                                                        form.delid.data), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_settings'))

            elif form.rename.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_settings'))

            elif form.delete.data and form.validate_on_submit():
                checkboxes = request.form.getlist('item_chb')

                if author is not None:
                    articles = Users.query.all()
                    n = None
                    for x in checkboxes:

                        # x is the unicode list thing which
                        # we convert to integer using regexp
                        x = int(re.search("\d+", str(x)).group())

                        for art_id in articles:
                            if art_id.id == x:
                                n = art_id.id
                        if x == n:
                            stmt = delete(Users).where(
                                Users.id == x)
                            conn.execute(stmt)
                            flash("Item {} is deleted!".format(x), 'info')
                        elif x == n:
                            flash("Item {} is exists".format(x), 'error')
                        else:
                            flash("Item {} is not deleted!".format(x), 'error')
                else:
                    return redirect(url_for('show_login'))
                return redirect(url_for('show_dashboard_settings'))

            elif form.delete.data is True and form.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_settings'))

        elif form_next.validate_on_submit():
            data = []
            data_array = sql.session.query(Users).filter(
                Users.login.match(form.query.data)).all()
            for x in data_array:
                data = x

            return jsonify(id=str(data.id),
                           login=data.login,
                           email=data.email,
                           date=data.regdate
                           )

        return render_template('adminboard/adminboard_settings.html',
                               form=form
                               )

    @app.route('/adminboard/adminboard_filemanager/', methods=['GET', 'POST'])
    def upload_file():
        form_mkdir = dashboard_filesform.DashboardMkdirForm()
        form_cddir = dashboard_filesform.DashboardCddirForm()
        form_upload = dashboard_filesform.DashboardUploadForm()
        form_files = dashboard_filesform.DashboardFilesForm()
        fileserving = FileBrowser()

        if request.method == 'POST':
            file = request.files['f_upload']

            # when working in upload context check if unwanted buttons are not pressed
            if (file.filename == ''
                    and form_cddir.cddir.data is False
                    and form_mkdir.mkdir.data is False
                    and form_files.rename.data is False
                    and form_files.delete.data is False
                    and form_upload.validate_on_submit()):
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            # check if the post request has the file part
            elif 'f_upload' not in request.files:
                flash('No file part')
                return redirect(request.url)

            # when working in upload context check if unwanted buttons are not pressed
            elif (file.filename
                  and form_cddir.cddir.data is False
                  and form_mkdir.mkdir.data is False
                  and form_files.rename.data is False
                  and form_files.delete.data is False
                  and form_upload.validate_on_submit()):

                # when working in upload context check if unwanted buttons are not pressed
                if (file.filename
                        and form_cddir.cddir.data is False
                        and form_mkdir.mkdir.data is False
                        and form_files.rename.data is False
                        and form_files.delete.data is False
                        and fileserving.allowed_file(file.filename)
                        and exists("{}{}".format(app.root_path,
                                                 request.form['addressbar']))):
                    filename = secure_filename(file.filename)
                    fpath = "{}{}{}".format(app.root_path, request.form['addressbar'], filename)
                    if filename and exists(fpath) is False:
                        file.save(fpath)
                        flash("{}{} is uploaded".format(request.form['addressbar'], filename), 'info')
                    elif exists(fpath):
                        flash("{}{} is exists".format(request.form['addressbar'], filename), 'error')
                    else:
                        flash("{}{} is not uploaded".format(request.form['addressbar'], filename), 'error')

                return redirect(url_for('show_dashboard_media'))

            elif (form_cddir.cddir.data
                  and form_cddir.validate_on_submit()):

                get_path = str(form_cddir.addressbar.data)

                if (exists("{}{}".format(app.root_path, get_path))
                        and isdir("{}{}".format(app.root_path, get_path))):

                    with open("{}/static/get_path.tmp".format(app.root_path), 'w') as f:
                        f.write(get_path)

                    fileserving.show_files(get_path)
                    flash("Location is changed to {} ".format(get_path), 'info')
                else:
                    flash("Location is not changed to {} ".format(get_path), 'error')
                return redirect(url_for('show_dashboard_media'))

            elif form_cddir.cddir.data is True and form_cddir.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            elif (form_mkdir.mkdir.data
                  and form_mkdir.validate_on_submit()):

                get_root_dirname = "{}{}".format(app.root_path, form_mkdir.addressbar.data)
                newdirname = form_mkdir.newdirname.data

                if exists(get_root_dirname) is True:
                    if exists("{}{}".format(get_root_dirname, newdirname)) is False and newdirname is not None:
                        fileserving.make_dir("{}{}".format(get_root_dirname, newdirname))
                        flash("Directory {}{} is created".format(get_root_dirname, newdirname), 'info')
                    elif exists("{}{}".format(get_root_dirname, newdirname)) is True and newdirname is not None:
                        flash("Directory {}{} is exists".format(get_root_dirname, newdirname), 'error')
                else:
                    flash("Directory {} is not exist. Please check the path".format(get_root_dirname), 'error')
                return redirect(url_for('show_dashboard_media'))

            elif form_mkdir.mkdir.data is True and form_mkdir.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            elif (form_files.rename.data
                  and form_files.validate_on_submit()):

                if (len(request.form.getlist('item_chb')) == 1
                        and len(request.form.getlist('delid')) == 1
                        and isinstance(request.form['addressbar'], unicode)):
                    old_object = "{}{}{}".format(app.root_path,
                                                 request.form['addressbar'],
                                                 request.form.get('item_chb'))
                    new_object = "{}{}{}".format(app.root_path,
                                                 request.form['addressbar'],
                                                 form_files.delid.data)

                    if exists(old_object):
                        fileserving.rename_file_dir(old_object, new_object)
                        flash("{} is renamed to {}".format(old_object,
                                                           new_object), 'info')
                    else:
                        flash("{} is not renamed to {}".format(old_object,
                                                               new_object), 'error')
                return redirect(url_for('show_dashboard_media'))

            elif form_files.rename.data is True and form_files.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            elif (form_files.delete.data
                  and form_files.validate_on_submit()):

                if (len(request.form.getlist('item_chb')) == 1
                        and isinstance(request.form['addressbar'], unicode)):
                    get_object = "{}{}{}".format(app.root_path,
                                                 request.form['addressbar'],
                                                 request.form['item_chb'])
                    if exists(get_object):
                        fileserving.del_file_dir(get_object)
                        flash("{} is deleted".format(get_object), 'info')
                    else:
                        flash("{} was not deleted".format(get_object), 'error')
                    return redirect(url_for('show_dashboard_media'))

            elif form_files.delete.data is True and form_files.validate_on_submit() is False:
                flash("No item selected", 'error')
                return redirect(url_for('show_dashboard_media'))

            return render_template('adminboard/adminboard_media.html',
                                   form=form_mkdir
                                   )

        return render_template('adminboard/adminboard_filemanager.html',
                               form=form_files
                               )
