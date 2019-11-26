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
from application.core.datalogics import Utils
from application.forms import dashboard_filesform
from flask_login import login_required
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify
from flask import url_for


@app.route('/adminboard/gfx_converter', methods=['GET', 'POST'])
@login_required
def gfx_converter():
    form = dashboard_filesform.GfxConvForm()

    if request.method == 'POST':
        if (form.conv_submit.data is True
                and form.validate_on_submit() is True
                and form.measure_submit.data is False):
            utils = Utils()
            file_name = request.form['item_chb']
            file_ext = file_name[len(file_name)-3:]
            if (file_name != ''
                    and file_ext != ''
                    and form.addressbar.data != ''
                    and form.fileformat.data != ''
                    and form.width.data != ''
                    and form.height.data != ''
            ):
                data = {'name': file_name,
                        'path': '{}{}'.format(app.root_path,
                                              form.addressbar.data),
                        'extension': file_ext,
                        'format': form.fileformat.data,
                        'width': form.width.data,
                        'height': form.height.data
                        }

                msg = utils.conv_image(data)
                if msg['status'] is 'OK':
                    flash(msg['message'], 'info')
                elif msg['status'] is 'ERROR':
                    flash(msg['message'], 'error')
            return redirect(url_for('show_dashboard_media'))

        elif (form.measure_submit.data is True
                and form.validate_on_submit() is True
                and form.conv_submit.data is False):
            utils = Utils()
            file_name = request.form['item_chb']
            file_ext = file_name[len(file_name)-3:]
            if (file_name != ''
                    and file_ext != ''
                    and form.addressbar.data != ''):
                data = {'name': file_name,
                        'path': '{}{}'.format(app.root_path,
                                              form.addressbar.data),
                        'extension': file_ext
                        }

                msg = utils.get_image_size(data)
                if msg['status'] is 'OK':
                    return jsonify(msg)
                elif msg['status'] is 'ERROR':
                    flash(msg['message'], 'error')
        return redirect(url_for('show_dashboard_media'))

    return render_template('adminboard/adminboard_media.html', form=form)
