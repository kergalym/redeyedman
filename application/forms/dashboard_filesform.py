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

from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired


class DashboardMkdirForm(Form):
    addressbar = TextField('addressbar', validators=[DataRequired()])
    newdirname = TextField('newdirname', validators=[DataRequired()])
    mkdir = SubmitField('mkdir')


class DashboardFilesForm(Form):
    addressbar = TextField('addressbar', validators=[DataRequired()])
    item_chb = BooleanField('item_chb', validators=[DataRequired()])
    delid = TextField('delid', validators=[DataRequired()])
    rename = SubmitField('rename')
    delete = SubmitField('delete')
    f_upload = SubmitField('f_upload')
    cddir = SubmitField('cddir')
    mkdir = SubmitField('mkdir')
