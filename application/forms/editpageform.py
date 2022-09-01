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


class EditpageAddForm(Form):
    id = StringField('id', validators=[DataRequired()])
    article_title = StringField('article_title', validators=[DataRequired()])
    article_author = StringField('article_author', validators=[DataRequired()])
    article_category = StringField('article_category', validators=[DataRequired()])
    article_date = StringField('article_date', validators=[DataRequired()])
    article_text = TextAreaField('article_text', validators=[DataRequired()])

