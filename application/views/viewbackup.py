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
from application.core.servicegate import Backup
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import url_for
from flask import g
import os


@app.route('/adminboard/backup')
@login_required
def do_backup():
    author = g.user
    backup = Backup()
    mysqldump_bin = os.path.abspath('/usr/bin/mysqldump')

    if (os.path.isfile(mysqldump_bin)
            and backup.db_backup() != "IOEror"
            and author is not None):
        msg = backup.db_backup()
        flash(msg, 'info')
        return redirect(url_for('show_dashboard_main'))
    else:
        flash("No tool for export the database or destination isn't exist. "
              "Please, contact to administrator", 'error')
        return redirect(url_for('show_dashboard_main'))
