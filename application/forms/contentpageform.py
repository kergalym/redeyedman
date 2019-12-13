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
from wtforms import TextField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class ContentpageAddForm(Form):
    id = TextField('id', validators=[DataRequired()])
    content_title = TextField('content_title', validators=[DataRequired()])
    content_author = TextField('content_author', validators=[DataRequired()])
    content_category = TextField('content_category', validators=[DataRequired()])
    content_date = TextField('content_date', validators=[DataRequired()])
    content_text = TextAreaField('content_text', validators=[DataRequired()])    
