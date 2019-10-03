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

from application.core.datalogics import Utils
from application import app
from application.forms import genpassform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import g


@app.route('/adminboard/editpage_id_users/', methods=['GET', 'POST'])
@login_required
def genpass():
    form = genpassform.DashboardGenPassForm()
    author = g.user
    utils = Utils()
    if author is not None \
            and request.method == 'POST' \
            and request.form.get('genpasswd', None) \
            and form.validate_on_submit():
        passwordphrase = utils.randomstr(int(request.form['passlength']))
        return render_template('adminboard/editpage_id_users.html',
                               form=form, passwordphrase=passwordphrase)
