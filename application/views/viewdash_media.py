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

from os.path import exists
from application import app
from application.core.datalogics import SysInfo
from application.core.datalogics import Paginator
from application.core.filemanagement import FileBrowser
from application.forms import dashboard_filesform
from flask_login import login_required
from flask import flash
from flask import abort
from flask import redirect
from flask import render_template
from flask import request
from flask import g
from flask import url_for
import socket
import os


@app.route('/adminboard/adminboard_media/')
@login_required
# TODO: user privilegies
def show_dashboard_media():
    browser = FileBrowser()
    per_page = 10
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

    if g.user != 'admin':
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

        if get_relpath == '':
            get_relpath = "/static/images/"

        files = browser.show_files(get_relpath)
        offset = ((pages - 1) * per_page)
        limit = per_page
        if pages == 0 or pages == 1:
            f = files[:limit]
        elif len(files)-offset > offset:
            f = files[limit:]
        elif len(files)-offset < offset:
            f = files[offset:]

        pagination = paginator.paginate_files(files, pages, per_page)
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
