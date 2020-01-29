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
from os import chdir

from application import app
from application.core.datalogics import SysInfo


class Backup:

    def __init__(self):
        self.backup_path = app.config['BACKUP_PATH']
        self.mysql_export_path = "{}/{}.sql".format(self.backup_path,
                                                    app.config['DBNAME'])
        self.site_path = os.path.split(self.backup_path)
        self.site_parent_path = app.root_path.strip('application')
        self.instance = SysInfo()
        self.file_output = "{}-{}.tar.gz".format(app.config['DBNAME'],
                                                 str(self.instance.altertime()))

    def db_backup(self):
        if (os.path.isdir(self.backup_path)
                and os.access(self.backup_path, os.W_OK)
                and os.path.isdir(self.site_parent_path)):
            command = 'mysqldump --opt -h {} -u {} -p{} {} > {}'.format(
                app.config['DBHOST'], app.config['DBUSERNAME'],
                app.config['DBPASSWORD'], app.config['DBNAME'],
                self.mysql_export_path)

            os.system(command)

            with tarfile.open("{}{}".format(self.backup_path, self.file_output),
                              "w:gz") as tar:
                tar.add(self.site_parent_path)
            return "Backup is created: {}".format(self.file_output)
        else:
            msg = "No correct data for export the database or destination/site parent path isn't exist.\n" \
                  "Backup Path: {}\n" \
                  "Backup Path Access: {}\n" \
                  "Please, contact to administrator \n".format(self.backup_path,
                                                               os.access(self.backup_path, os.W_OK))
            return msg
