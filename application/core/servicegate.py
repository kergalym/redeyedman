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

import os
import tarfile
from application import app
from application.core.datalogics import SysInfo


class Backup:

    def db_backup(self):
        backup_path = app.root_path
        mysql_export_path = "{}/backup/{}.sql".format(app.root_path, app.config['DBNAME'])
        site_path = os.path.split(backup_path)
        instance = SysInfo()

        if (os.path.isdir('{}/backup'.format(backup_path))
                and os.access('{}/backup'.format(backup_path), os.W_OK)):
            command = 'mysqldump --opt -h {} -u {} -p{} {} > {}'.format(
                app.config['DBHOST'], app.config['DBUSERNAME'],
                app.config['DBPASSWORD'], app.config['DBNAME'],
                mysql_export_path)

            os.system(command)

            with tarfile.open(app.config['DBNAME'] + '-'
                              + str(instance.altertime()) + '.tar.gz', "w:gz") as tar:
                tar.add(site_path[-2],
                        arcname=os.path.basename(backup_path))
        else:
            # print "No tool for export the database or destination isn't exist. " \
            # + "Please, contact to administrator"
            return "IOEror"
