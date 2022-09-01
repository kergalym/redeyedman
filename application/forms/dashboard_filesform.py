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
from wtforms import StringField, SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired


class DashboardMkdirForm(Form):
    addressbar = StringField('addressbar', validators=[DataRequired()])
    newdirname = StringField('newdirname', validators=[DataRequired()])

    mkdir = SubmitField('mkdir')


class DashboardCddirForm(Form):
    addressbar = StringField('addressbar', validators=[DataRequired()])

    cddir = SubmitField('cddir')


class DashboardUploadForm(Form):
    addressbar = StringField('addressbar', validators=[DataRequired()])
    f_upload = BooleanField('f_upload')


class DashboardFilesForm(Form):
    f_upload = BooleanField('f_upload')
    addressbar = StringField('addressbar', validators=[DataRequired()])
    item_chb = BooleanField('item_chb', validators=[DataRequired()])
    delid = StringField('delid', validators=[DataRequired()])

    f_rename = SubmitField('f_rename')
    f_delete = SubmitField('f_delete')


class GfxConvForm(Form):
    addressbar = StringField('addressbar', validators=[DataRequired()])
    width = StringField('width', validators=[DataRequired()])
    height = StringField('height', validators=[DataRequired()])
    fileformat = StringField('fileformat', validators=[DataRequired()])
    qrange = StringField('qrange', validators=[DataRequired()])
    item_chb = BooleanField('item_chb', validators=[DataRequired()])

    conv_submit = SubmitField('conv_submit')
    measure_submit = SubmitField('measure_submit')


class GetSelectedFileForm(Form):
    addressbar = StringField('addressbar', validators=[DataRequired()])
    item_chb = BooleanField('item_chb', validators=[DataRequired()])
