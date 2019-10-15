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
import shutil

from application import app, ALLOWED_EXTENSIONS
from os import stat
from os import path
from os import rename
from os import remove, rmdir
from os import mkdir
from os import getcwd
from os import listdir
from os import chmod
from os.path import isdir
from os.path import isfile
from os.path import join
from datetime import datetime


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

    def allowed_file(self, filename):
        self.filename = filename
        return '.' in self.filename and \
               self.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def array_slice(self, array, offset, length=None):
        if isinstance(array, list) and not isinstance(array, dict):
            if isinstance(array, set):
                array = list(array)
                return set(array[offset:length])
            return array[offset:length]
        return False

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
        # TODO:
        # shutil.copytree and shutil.move

    def hsize(self, sbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        i = 0
        # import pdb; pdb.set_trace()
        self.sbytes = sbytes

        while self.sbytes >= 1024 and i < len(suffixes) - 1:
            sbytes /= 1024.
            i += 1
        f = ('%.2f' % sbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])

    def polystat(self, object, attribute):
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
            return uid.st_uid
        else:
            return False

    def show_files(self, get_path):
        self.get_path = get_path
        files = []
        if isinstance(self.get_path, str):
            # Delete first slash for join
            self.get_path = self.get_path.lstrip('/')
            if isdir(join(app.root_path, self.get_path)):
                f_list = listdir(join(app.root_path, self.get_path))
                for num, file_x, in enumerate(f_list, 1):
                    inner = [
                        {"id": "{}".format(
                            num),
                            "relpath": "/{}{}".format(
                                self.get_path, file_x
                            ),
                            "name": "{}".format(
                                file_x
                            ),
                            "owner": self.polystat("{}/{}/{}".format(
                                app.root_path, self.get_path, file_x),
                                'st_uid'
                            ),
                            "size": self.hsize(
                                path.getsize("{}/{}/{}".format(
                                    app.root_path, self.get_path, file_x))),
                            "date": self.polystat("{}/{}/{}".format(
                                app.root_path, self.get_path, file_x),
                                'st_ctime'
                            ),
                            "perm": self.polystat("{}/{}/{}".format(
                                app.root_path, self.get_path, file_x),
                                'st_mode'
                            )}
                    ]
                    files += inner
                return files
        else:
            return "{} is not a directory".format(self.get_path)

    def change_own(self, get_path):
        self.get_path = get_path
        if isinstance(self.get_path, str):
            return chmod(self.get_path)
        elif isinstance(self.get_path, list):
            for files in self.get_path:
                per_file = files
                per_path = getcwd(self.get_path)
                if isinstance(per_file, str) and isinstance(per_path, str):
                    file_array = "{}/{}".format(per_path, per_file)
                    chmod(file_array)
                else:
                    break
                return "input objects are not strings"
        else:
            return "Incorrect input object"
