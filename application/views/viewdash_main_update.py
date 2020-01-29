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
from application import app
from application import sql
from application import engine
from sqlalchemy import update
from sqlalchemy import delete
from application.core.dbmodel import Articles
from application.forms import dashboard_itemsform
from application.forms import dashboard_searchform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for
from flask import g
from sqlalchemy import exc


@app.route('/adminboard/adminboard_main/', methods=['GET', 'POST'])
@login_required
def update_dashboard_main():
    form = dashboard_itemsform.DashboardItemsForm()
    form_next = dashboard_searchform.DashboardSearchForm()
    author = g.user
    conn = engine.connect()

    if request.method == 'POST':
        if form.rename.data and form.validate_on_submit():
            checkboxes = request.form.getlist('item_chb')

            # form.delid.data is the unicode list thing which
            # we convert to integer using regexp
            delid = int(re.search("\d+", str(form.delid.data)).group())

            if author is not None:
                articles = Articles.query.all()
                n = None
                for x in checkboxes:

                    # x is the unicode list thing which
                    # we convert to integer using regexp
                    x = int(re.search("\d+", str(x)).group())

                    for art_id in articles:
                        if art_id.id == x:
                            n = art_id.id
                    if x == n and x != delid:
                        stmt = update(Articles).where(
                            Articles.id == x
                        ).values(
                            id=delid
                        )
                        try:
                            conn.execute(stmt)
                            conn.close()
                            flash("Item {} is changed to {}".format(x,
                                                                    form.delid.data), 'info')
                        except exc.IntegrityError:
                            flash("Item {} is exists".format(delid), 'error')
                    elif x == delid:
                        flash("Item {} is exists".format(delid), 'error')
                    else:
                        flash("Item {} is not changed to {}".format(x,
                                                                    form.delid.data), 'error')
            else:
                return redirect(url_for('show_login'))
            return redirect(url_for('show_dashboard_main'))

        elif form.rename.data is True and form.validate_on_submit() is False:
            flash("No item selected", 'error')
            return redirect(url_for('show_dashboard_main'))

        elif form.delete.data and form.validate_on_submit():
            checkboxes = request.form.getlist('item_chb')

            if author is not None:
                articles = Articles.query.all()
                n = None
                for x in checkboxes:

                    # x is the unicode list thing which
                    # we convert to integer using regexp
                    x = int(re.search("\d+", str(x)).group())

                    for art_id in articles:
                        if art_id.id == x:
                            n = art_id.id
                    if x == n:
                        stmt = delete(Articles).where(
                            Articles.id == x)
                        conn.execute(stmt)
                        conn.close()
                        flash("Item {} is deleted!".format(x), 'info')
                    elif x == n:
                        flash("Item {} is exists".format(x), 'error')
                    else:
                        flash("Item {} is not deleted!".format(x), 'error')
            else:
                return redirect(url_for('show_login'))
            return redirect(url_for('show_dashboard_main'))

        elif form.delete.data is True and form.validate_on_submit() is False:
            flash("No item selected", 'error')
            return redirect(url_for('show_dashboard_main'))

        elif form_next.validate_on_submit():
            data = []
            data_array = sql.session.query(Articles).filter(
                Articles.article_title.match(form_next.query.data)).all()
            if data_array:
                for x in data_array:
                    data = x

                return jsonify(id=str(data.id),
                               title=data.article_title,
                               author=data.article_author,
                               category=data.article_category,
                               date=data.article_date,
                               published=data.published
                               )
            else:
                return redirect(url_for('show_dashboard_main'))

    return render_template('adminboard/adminboard_main.html',
                           form=form
                           )
