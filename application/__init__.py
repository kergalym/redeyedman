# -*- coding: UTF-8 -*-

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

from flask import Flask
from flask_debug import Debug
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
import sys

# Set encoding to UTF-8 hack
reload(sys)
sys.setdefaultencoding('utf-8')

# Define the app object and load the config from the file
app = Flask(__name__)
app.secret_key = 'unique_GtwAhENew8ghtsgWK'
app.config.from_object('configuration')
app.debug = False

# Read database settings from the configuration file
dbhost = app.config['DBHOST']
dbname = app.config['DBNAME']
dbuser = app.config['DBUSERNAME']
dbpass = app.config['DBPASSWORD']

# File uplad params
UPLOAD_FOLDER = '/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# Set the SQLAlchemy connection string to our database using provided information.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % \
                                        (dbuser, dbpass, dbhost, dbname)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_size=30, max_overflow=0)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
sql = SQLAlchemy(app)

# Make session
session = sessionmaker()
session.configure(bind=engine)
session_timein = app.permanent_session_lifetime

# Debug
Debug(app)
toolbar = DebugToolbarExtension(app)


# Import views to enable proper routing
from application.core import dbmodel
from application.core.datalogics import Base

from application.views import viewapp

from application.views import viewdash_login_logout

from application.views import viewdash
from application.views import viewdash_main
from application.views import viewdash_inner
from application.views import viewdash_media
from application.views import viewdash_category
from application.views import viewdash_users
from application.views import viewdash_filemanager

from application.views import viewdash_main_update
from application.views import viewdash_inner_update
from application.views import viewdash_media_update
from application.views import viewdash_media_gfx_converter_update
from application.views import viewdash_pub
from application.views import viewdash_category_update
from application.views import viewdash_users_update
from application.views import viewdash_filemanager_update
from application.views import viewdash_forgot_password_update

from application.views import viewedit
from application.views import viewedit_content
from application.views import viewedit_category
from application.views import viewedit_id
from application.views import vieweditcontent_id
from application.views import vieweditcategory_id
from application.views import vieweditusers_id

from application.views import viewbackup

from application.views import viewuseradd
