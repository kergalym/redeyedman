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

from application import app, ALLOWED_EXTENSIONS
from application.core.datalogics import SysInfo
from os import stat
from os import rename
from os import remove
from os import mkdir
from os import getcwd
from os import listdir
from os import chmod
from os.path import isdir
from os.path import isfile
from datetime import datetime
from pwd import getpwuid
import shutil


class FileBrowser:

    def __init__(self):
        self.get_dirname = app.root_path
        self.filename = None
        self.old_object = None
        self.new_object = None
        self.obj = None
        self.attr = None
        self.get_path = None
        self.sbytes = None
        self.sysinfo = SysInfo()

    def allowed_file(self, filename):
        self.filename = filename
        return '.' in self.filename and \
               self.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def make_dir(self, get_dirname):
        self.get_dirname = get_dirname
        if type(self.get_dirname) == str:
            return mkdir(self.get_dirname)
        else:
            return False

    def rename_file_dir(self, old_object, new_object):
        self.old_object = old_object
        self.new_object = new_object
        if (isinstance(self.old_object, str)
                and isinstance(self.new_object, str)):
            return rename(self.old_object, self.new_object)
        else:
            return False

    def del_file_dir(self, get_path):
        self.get_dirname = get_path
        if isinstance(self.get_dirname, str):
            if isdir("{}".format(self.get_dirname)):
                return shutil.rmtree(self.get_dirname)
            elif isfile("{}".format(self.get_dirname)):
                return remove("{}".format(self.get_dirname))
        else:
            return False

    def move_file_dir(self, get_path):
        pass
        # TODO: shutil.copytree and shutil.move

    def file_size(self, file_path):
        """
        Return the file size
        """
        if isfile(file_path):
            file_info = stat(file_path)
            return self.sysinfo.conv_bytes(file_info.st_size)

    def file_attr(self, object, attribute):
        """
        Return file attributes
        """
        self.obj = object
        self.attr = attribute
        if self.attr == 'st_ctime':
            ct = stat(self.obj)
            return "{}".format(datetime.fromtimestamp(ct.st_ctime))
        elif self.attr == 'st_mode':
            mo = stat(self.obj)
            return oct(mo.st_mode)[-3:]
        elif self.attr == 'st_uid':
            uid = stat(self.obj)
            return getpwuid(uid.st_uid).pw_name
        else:
            return False

    def show_files(self, get_path):
        """
        Shows files for the dashboard media section
        """
        # get_path is unicode string, make it simple string
        self.get_path = str(get_path)

        files = []

        if (isinstance(self.get_path, str)
                and isdir("{}{}".format(app.root_path, self.get_path))):

            # if no slash at the end of path
            if self.get_path.endswith("/") is False:
                self.get_path = "{}/".format(self.get_path)

            f_list = listdir("{}{}".format(app.root_path, self.get_path))
            for num, file_x, in enumerate(f_list, 1):
                inner = [
                    {"id": "{}".format(
                        num),
                        "relpath": "{}{}".format(
                            self.get_path, file_x
                        ),
                        "name": "{}".format(
                            file_x
                        ),
                        "owner": self.file_attr("{}/{}{}".format(
                            app.root_path, self.get_path, file_x),
                            'st_uid'
                        ),
                        "size": self.file_size(("{}/{}{}".format(
                            app.root_path, self.get_path, file_x))),
                        "date": self.file_attr("{}/{}{}".format(
                            app.root_path, self.get_path, file_x),
                            'st_ctime'
                        ),
                        "perm": self.file_attr("{}/{}{}".format(
                            app.root_path, self.get_path, file_x),
                            'st_mode'
                        )}
                ]
                files += inner
            return files

    def change_own(self, get_path):
        """
        Change file owner & permissions
        """
        self.get_path = get_path
        if isinstance(self.get_path, str):
            return chmod(self.get_path)
        elif isinstance(self.get_path, list):
            for files in self.get_path:
                per_file = files
                per_path = getcwd()
                if isinstance(per_file, str) and isinstance(per_path, str):
                    file_array = "{}/{}".format(per_path, per_file)
                    chmod(file_array)
                else:
                    break
                return "input objects are not strings"
        else:
            return "Incorrect input object"
