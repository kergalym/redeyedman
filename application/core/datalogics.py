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
from random import randrange
from datetime import datetime
from application import app
from application.core.dbmodel import Users
from application import login_manager
from flask_login import login_required
from flask_paginate import Pagination
from passlib.hash import pbkdf2_sha256
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
                text = rawtext[0:self.maxlength] + " ... "
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

    def paginate(self, class_name, pages, per_page):
        self.class_name = class_name
        self.pages = pages
        self.per_page = per_page
        if hasattr(self.class_name, 'query') is True:
            totalrecords = len(self.class_name.query.all())
        elif isinstance(self.class_name, list):
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

    @login_required
    def hash_password(self, password):
        return pbkdf2_sha256.encrypt(password, rounds=25600)

    @login_required
    def verify_password(self, password, hash):
        return pbkdf2_sha256.verify(password, hash)

    @login_required
    def randomstr(self, passlength):
        self.passlength = passlength
        keyspace = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        pwstring = ''
        maxlen = len(keyspace)

        try:
            passlength < 1
        except Warning:
            print "Keyspace must be long"

        for i in range(self.passlength):
            pwstring = pwstring + keyspace[randrange(maxlen)]

        return pwstring


class SysInfo(Base):
    def __init__(self):
        self.localtime = None
        self.alterlocaltime = None

    @login_required
    def humanize_bytes(self, bytes, precision=1):
        """Return a humanized string representation of a number of bytes.

        Assumes `from __future__ import division`.

        >>> humanize_bytes(1)
        '1 byte'
        >>> humanize_bytes(1024)
        '1.0 kB'
        >>> humanize_bytes(1024*123)
        '123.0 kB'
        >>> humanize_bytes(1024*12342)
        '12.1 MB'
        >>> humanize_bytes(1024*12342,2)
        '12.05 MB'
        >>> humanize_bytes(1024*1234,2)
        '1.21 MB'
        >>> humanize_bytes(1024*1234*1111,2)
        '1.31 GB'
        >>> humanize_bytes(1024*1234*1111,1)
        '1.3 GB'
        """
        abbrevs = (
            (1 << 50L, 'PB'),
            (1 << 40L, 'TB'),
            (1 << 30L, 'GB'),
            (1 << 20L, 'MB'),
            (1 << 10L, 'kB'),
            (1, 'bytes')
        )

        if bytes == 1:
            return '1 byte'
        for factor, suffix in abbrevs:
            if bytes >= factor:
                break
            return '%.*f %s' % (precision, bytes / factor, suffix)

    @login_required
    def diskspace(self):
        f = os.statvfs(app.root_path)
        estimate = f
        output = (estimate.f_bavail * estimate.f_frsize) / 1024
        return output

    @login_required
    def systime(self):
        self.localtime = str(time.asctime(time.localtime()))
        return self.localtime

    @login_required
    def altertime(self):
        self.alterlocaltime = str(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S"))
        return self.alterlocaltime
