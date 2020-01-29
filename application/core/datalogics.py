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
import time
import re
from os.path import exists
from os.path import isfile
from random import randrange
from datetime import datetime

from PilLite import Image

from application import app, bcrypt
from application.core.dbmodel import Users
from application import login_manager
from flask_login import login_required
from flask_paginate import Pagination
from flask import request


class Base:

    @login_manager.user_loader
    def load_user_login(login):
        token = request.headers.get('Authorization')
        if token is None:
            token = request.args.get('token')

            return Users.query.get(login)

        if token is not None:
            login, password = token.split(":")
            user_entry = Users.query.get(login)
            if user_entry is not None:
                user = Users(user_entry[0], user_entry[1])
                if user.password == password:
                    return user


class Dlogics(Base):
    def __init__(self):
        self.row = None
        self.maxlength = 320

    def textcutn(self, row):
        self.row = row
        content = ''
        # Find the beginning tag
        btag_pattern = r'\\r\\n<.*?>|<.*?>|<h.*?>'
        # Find end tag from btag
        etagn_pattern = r'(<\/.*?>\\r\\n\\r\\n)|(<\/.*?>\\r\\n)|(<\/.*?>)|<\/h.*?>'
        # Do handling: strip from tags in etag
        rawtext_pattern = r'(<.*?>)|(<\/.*?>)(\\r\\n\\r\\n)|(<\/.*?>\\r\\n)|<\/h.*?>'

        if isinstance(self.row, unicode) and isinstance(self.maxlength, int):
            # Find the beginning tag
            btag = re.match(btag_pattern, self.row).group(0)
            # Find end tag
            etag = re.search(etagn_pattern, self.row[len(btag):]).group(0)
            # Do handling: strip from tags in btag:
            # slicing to the remaining part of the string
            # and replacing pattern by empty space

            rawtext = unicode(re.sub(rawtext_pattern, '', self.row[len(btag):]))

            if len(rawtext) >= self.maxlength:
                # Replace with a part of unicode string
                text = rawtext[0:self.maxlength] + "..."
                prepared = "{}{}{}".format(btag, text, etag)
                content += unicode(prepared)
                return content
            else:
                # Get the first part of the row
                self.row = self.row[len(self.row):]
                # Send the last part of the row
                content = self.row
            return content
        else:
            return "Row {} is not unicode string".format(type(self.row))


class Paginator(Base):
    def __init__(self):
        self.class_name = None
        self.pages = None
        self.per_page = None

    def paginate_queries(self, class_name, pages, per_page):
        self.class_name = class_name
        self.pages = pages
        self.per_page = per_page

        if hasattr(self.class_name, 'query') is True:
            totalrecords = len(self.class_name.query.all())
        else:
            return "{} is not a list".format(self.class_name)
        pagination = Pagination(page=self.pages, total=totalrecords,
                                per_page=self.per_page,
                                alignment="center",
                                css_framework='bootstrap')
        return pagination

    def paginate_files(self, class_name, pages, per_page):
        self.class_name = class_name
        self.pages = pages
        self.per_page = per_page

        if isinstance(self.class_name, list):
            totalrecords = len(self.class_name)
        else:
            return "{} is not a list".format(self.class_name)
        pagination = Pagination(page=self.pages, total=totalrecords,
                                per_page=self.per_page,
                                css_framework='bootstrap')
        return pagination


class Utils(Base):
    def __init__(self):
        self.passlength = None

    def hash_password(self, password):
        return bcrypt.generate_password_hash(password)

    def verify_password(self, password, hash):
        return bcrypt.check_password_hash(hash, password)

    def randomstr(self, passlength):
        self.passlength = passlength
        keyspace = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        pwstring = ''
        maxlen = len(keyspace)

        try:
            passlength < 1
        except Warning:
            return "Keyspace must be long"

        for i in range(self.passlength):
            pwstring = pwstring + keyspace[randrange(maxlen)]

        return pwstring

    def abc_randomizer(self):
        abc = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e",
               5: "f", 6: "g", 7: "h", 8: "i", 9: "j",
               10: "k", 11: "l", 12: "m", 13: "n",
               14: "o", 15: "p", 16: "q", 17: "r",
               18: "s", 19: "t", 20: "u", 21: "v",
               22: "w", 23: "x", 24: "y", 25: "z"
               }
        return abc

    @login_required
    def conv_image(self, data):
        if isinstance(data, dict):
            img_file = data['name']
            img_path = data['path']
            new_format = data['format']
            new_width = data['width']
            new_height = data['height']
            size = new_width, new_height
            outfile = "{}{}{}".format(img_path, str(img_file[:len(img_file) - 3]), str(new_format.lower()))
            origfile = "{}{}".format(img_path, str(img_file))

            if (isinstance(data, dict)
                    and exists("{}{}".format(img_path, img_file)) is True
                    and isfile("{}{}".format(img_path, img_file)) is True
                    and outfile is not origfile):
                try:
                    if img_file[len(img_file) - 3:] == 'png' or 'jpg' or 'jpeg':
                        img = Image.open("{}{}".format(img_path, img_file))
                        img.thumbnail(size)
                        img.save(outfile, new_format)
                        return {'status': "OK",
                                'message': "Original file is converted to {}".format(
                                    outfile)}
                except IOError:
                    return {'status': "ERROR",
                            'message': "Original file is not changed"}

    @login_required
    def get_image_size(self, data):
        if isinstance(data, dict):
            img_file = data['name']
            img_path = data['path']
            if (exists("{}{}".format(img_path, img_file))
                    and isfile("{}{}".format(img_path, img_file))):
                if img_file[len(img_file) - 3:] == 'png' or 'jpg' or 'jpeg':
                    try:
                        img = Image.open("{}{}".format(img_path, img_file))
                        size = img.size
                        width = int(re.search("\d+", str(size[0])).group())
                        height = int(re.search("\d+", str(size[1])).group())

                        return {'status': "OK",
                                'message': "Original file is found",
                                'width': width,
                                'height': height
                                }

                    except IOError:
                        return {'status': "ERROR",
                                'message': "Original file is not found"
                                }
                else:
                    return {'status': "ERROR",
                            'message': "Original file is not supported: {}".format(img_file[len(img_file) - 3:])
                            }


class SysInfo(Base):
    def __init__(self):
        self.localtime = None
        self.alterlocaltime = None

    @login_required
    def conv_bytes(self, num):
        """
        Convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "{} {}".format(round(float(num), 1), x)
            num /= 1024.0

    @login_required
    def diskspace(self):
        """
        Return free disk space
        """
        f = os.statvfs(app.root_path)
        estimate = f
        output = (estimate.f_bavail * estimate.f_frsize)
        return self.conv_bytes(output)

    @login_required
    def systime(self):
        self.localtime = str(time.asctime(time.localtime()))
        return self.localtime

    @login_required
    def altertime(self):
        self.alterlocaltime = str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S"))
        return self.alterlocaltime
