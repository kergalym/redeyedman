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

from os.path import exists, isdir
from werkzeug.utils import secure_filename
from application import app
from application.core.filemanagement import FileBrowser
from application.forms import dashboard_filesform
from flask_login import login_required
from flask import send_from_directory
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for


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
        file = request.files.get('f_upload')

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

            get_path = str(form_files.addressbar.data)

            # if no slash at the end of path
            if get_path.endswith("/") is False:
                get_path = "{}/".format(get_path)

            # when working in upload context check if unwanted buttons are not pressed
            if (file.filename
                    and form_cddir.cddir.data is False
                    and form_mkdir.mkdir.data is False
                    and form_files.rename.data is False
                    and form_files.delete.data is False
                    and fileserving.allowed_file(file.filename)
                    and exists("{}{}".format(app.root_path,
                                             get_path))):
                filename = secure_filename(file.filename)
                fpath = "{}{}{}".format(app.root_path, get_path, filename)
                if filename and exists(fpath) is False:
                    file.save(fpath)
                    flash("{} is uploaded".format(filename), 'info')
                elif exists(fpath):
                    flash("{} is exists".format(filename), 'error')
                else:
                    flash("{} is not uploaded".format(filename), 'error')

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
            addressbar = form_mkdir.addressbar.data
            if addressbar.endswith("/") is False:
                addressbar = "{}/".format(addressbar)
            get_root_dirname = "{}{}".format(app.root_path, addressbar)
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

                get_path = str(form_files.addressbar.data)

                # if no slash at the end of path
                if get_path.endswith("/") is False:
                    get_path = "{}/".format(get_path)

                old_object = "{}{}{}".format(app.root_path,
                                             get_path,
                                             request.form.get('item_chb'))
                new_object = "{}{}{}".format(app.root_path,
                                             get_path,
                                             form_files.delid.data)

                if exists(old_object):
                    fileserving.rename_file_dir(old_object, new_object)
                    flash("{} is renamed to {}".format(request.form.get('item_chb'),
                                                       form_files.delid.data), 'info')
                else:
                    flash("{} is not renamed to {}".format(request.form.get('item_chb'),
                                                           form_files.delid.data), 'error')
                return redirect(url_for('show_dashboard_media'))

        elif form_files.rename.data is True and form_files.validate_on_submit() is False:
            flash("No item selected", 'error')
            return redirect(url_for('show_dashboard_media'))

        elif (form_files.delete.data
              and form_files.validate_on_submit()):

            if (len(request.form.getlist('item_chb')) == 1
                    and isinstance(request.form['addressbar'], unicode)):

                get_path = str(form_files.addressbar.data)

                # if no slash at the end of path
                if get_path.endswith("/") is False:
                    get_path = "{}/".format(get_path)

                get_object = "{}{}{}".format(app.root_path,
                                             get_path,
                                             request.form['item_chb'])
                if exists(get_object):
                    fileserving.del_file_dir(get_object)
                    flash("{} is deleted".format(request.form['item_chb']), 'info')
                else:
                    flash("{} was not deleted".format(request.form['item_chb']), 'error')
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
