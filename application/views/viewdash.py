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
from application.core.datalogics import SysInfo
from flask_login import login_required
from flask import flash
from flask import render_template
from flask import current_app
from flask import g
from flask_login import current_user
import socket
import os


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
