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
from application import sql
from application.core.dbmodel import Content
from application.core.dbmodel import Categories
from application.core.datalogics import SysInfo
from application.forms import contentpage_idform
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

#
#   ARTICLES EDITPAGE ADD
#


@app.route('/adminboard/editpage_id_content/<int:id>', methods=['GET', 'POST'])
#@login_required
def show_contentpageid(id):
    form = contentpage_idform.ContentpageidForm()
    editpage_output_loop = Content.query.filter_by(id=id).first()
    categories_loop = Categories.query.all()
    instance = SysInfo()
    atime = instance.altertime() 
    author = session['login']
    if editpage_output_loop and categories_loop \
        and atime and author is not None:
        return render_template(
                                'adminboard/editpage_id_content.html', 
                                author=author, atime=atime, 
                                editpage_output_loop=editpage_output_loop,
                                categories_loop=categories_loop,
                                form=form)
    else:
        return redirect(url_for('show_login'))
    
@app.route('/adminboard/editpage_id_content/', methods=['GET', 'POST'])
#@login_required
def update_contentpageid():
    error = None
    form = contentpage_idform.ContentpageidForm()
    author = session['login']
    if request.method == 'POST' and form.validate_on_submit():
        if author is not None:
            content_id = request.form['content_id']                
            content_title = request.form['content_title']
            content_author = request.form['content_author']
            content_category = request.form['content_category']
            content_date = request.form['content_date']
            content_text = request.form['content_text']
            contents = Content(content_id, content_title, content_author, 
            content_category, content_date, content_text)
            sql.session.add(contents)
            sql.session.commit()
            error = "Content is changed"
            return redirect(url_for('show_contentpageid', id=request.form['content_id']))
    else:
        error = "Content is not changed"
        return redirect(url_for('show_contentpageid'))
    return render_template('adminboard/editpage_id_content.html',  
                            form=form, error=error
                            ) 
                       