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
from application import engine
from sqlalchemy import update
from application.core.dbmodel import Articles, Content
from application.forms import pubswitch_form
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import g


@app.route('/adminboard/pub_switcher_main', methods=['GET', 'POST'])
@login_required
def pub_switcher_main():
    form = pubswitch_form.PubSwitchForm()
    author = g.user
    conn = engine.connect()

    if (request.method == 'POST'
            and request.form.getlist('item_chb') == 1
            and author is not None
            and form.validate_on_submit()):
        stmt = update(Articles).where(
            Articles.id == request.form['item_chb']
        ).values(
            published=form.published.data
        )
        conn.execute(stmt)
        conn.close()

        if int(form.published.data) == 1:
            flash("Item {} is published".format(request.form['item_chb']), 'info')
        elif int(form.published.data) == 0:
            flash("Item {} is unpublished".format(request.form['item_chb']), 'warn')

        return redirect(url_for('show_dashboard_main'))

    elif (request.method == 'POST'
          and request.form.getlist('item_chb') > 1
            and author is not None
            and form.validate_on_submit()):
        for i in request.form.getlist('item_chb'):
            stmt = update(Articles).where(
                Articles.id == int(i)
            ).values(
                published=form.published.data
            )
            conn.execute(stmt)
        conn.close()

        s = ''
        for i in request.form.getlist('item_chb'):
            s += " {} ".format(i)

        if int(form.published.data) == 1:
            flash("{} items are published".format(s), 'info')
        elif int(form.published.data) == 0:
            flash("{} items are unpublished".format(s), 'warn')

        return redirect(url_for('show_dashboard_main'))

    else:
        flash("Item(s) is not changed", 'error')
        return redirect(url_for('show_dashboard_main'))


@app.route('/adminboard/pub_switcher_inner', methods=['GET', 'POST'])
@login_required
def pub_switcher_inner():
    form = pubswitch_form.PubSwitchForm()
    author = g.user
    conn = engine.connect()

    if (request.method == 'POST'
            and request.form.getlist('item_chb') == 1
            and author is not None
            and form.validate_on_submit()):
        stmt = update(Content).where(
            Content.id == request.form['item_chb']
        ).values(
            published=form.published.data
        )
        conn.execute(stmt)
        conn.close()

        if int(form.published.data) == 1:
            flash("Item {} is published".format(request.form['item_chb']), 'info')
        elif int(form.published.data) == 0:
            flash("Item {} is unpublished".format(request.form['item_chb']), 'warn')

        return redirect(url_for('show_dashboard_inner'))

    elif (request.method == 'POST'
          and request.form.getlist('item_chb') > 1
            and author is not None
            and form.validate_on_submit()):
        for i in request.form.getlist('item_chb'):
            stmt = update(Content).where(
                Content.id == int(i)
            ).values(
                published=form.published.data
            )
            conn.execute(stmt)
        conn.close()

        s = ''
        for i in request.form.getlist('item_chb'):
            s += " {} ".format(i)

        if int(form.published.data) == 1:
            flash("{} items are published".format(s), 'info')
        elif int(form.published.data) == 0:
            flash("{} items are unpublished".format(s), 'warn')

        return redirect(url_for('show_dashboard_inner'))

    else:
        flash("Item(s) is not changed", 'error')
        return redirect(url_for('show_dashboard_inner'))
