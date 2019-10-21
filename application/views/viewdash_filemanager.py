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
import socket

from application import app
from application.core.datalogics import Paginator, SysInfo
from application.core.dbmodel import Articles
from application.core.filemanagement import FileBrowser
from application.views.viewdash import ViewDash
from application.forms import dashboard_filesform
from flask_login import login_required
from flask import request, g, render_template


class ViewdashFileManager(ViewDash):

    @app.route('/adminboard/adminboard_media/')
    @login_required
    def show_dashboard_media():
        browser = FileBrowser()
        per_page = 9
        pages = request.args.get('page', type=int, default=1)
        paginator = Paginator()
        articles_loop = []
        form = dashboard_filesform.DashboardMkdirForm()
        servername = socket.gethostname()
        approot = os.path.split(app.root_path)
        users = g.user
        instance = SysInfo()
        freespace = instance.diskspace()
        ltime = instance.systime()
        atime = instance.altertime()
        if not users and pages == None:
            os.abort(404)
        else:
            articles_loop = sql.session.query(Articles).limit(
                (per_page)).offset(
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

        form = dashboard_filesform.DashboardMkdirForm()

        if (request.method == 'POST' and request.form.get('rename', None)
                and form.validate_on_submit()):
            pass
