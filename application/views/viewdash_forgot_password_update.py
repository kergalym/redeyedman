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

from application.core.datalogics import Utils
from application.core.dbmodel import Articles
from application.core.dbmodel import Categories
from application.core.dbmodel import Content
from application.core.dbmodel import Users
from application.core.filemanagement import FileBrowser
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
from sqlalchemy import exc


@app.route('/login/', methods=['GET', 'POST'])
@login_required
# TODO: add arg self to the decorator
# TODO: forgot_password() viewpooint
def forgot_password():
    pass

    """return render_template('adminboard/login.html',
                               form=form
                               )

    return render_template('adminboard/login.html',
                           form=form
                           )"""
