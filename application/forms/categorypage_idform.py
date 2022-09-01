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
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class CategorypageidForm(Form):
    id = StringField('id', validators=[DataRequired()])
    category_title = StringField('category_title', validators=[DataRequired()])
    category_author = StringField('category_author')
    category_date = StringField('category_date', validators=[DataRequired()])
    category_desc = TextAreaField('category_desc')
