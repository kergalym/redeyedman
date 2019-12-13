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

from __future__ import division
from sqlalchemy import Column, Integer, String
from application import sql
from flask_login import UserMixin


class Articles(sql.Model):
    __tablename__ = 'articles'

    id = sql.Column(Integer, primary_key=True, nullable=False)
    article_title = sql.Column(String, index=True, unique=True, nullable=False)
    article_author = sql.Column(String, nullable=False)
    article_category = sql.Column(String, nullable=False)
    article_date = sql.Column(String, nullable=False)
    article_mod_date = sql.Column(String, nullable=False)
    article_text = sql.Column(String, nullable=False)
    published = sql.Column(Integer, nullable=False)

    def __init__(
                self, id, article_title, 
                article_author, article_category, 
                article_date, article_mod_date,
                article_text, published):
        self.id = id                    
        self.article_title = article_title
        self.article_author = article_author
        self.article_category = article_category
        self.article_date = article_date
        self.article_mod_date = article_mod_date
        self.article_text = article_text
        self.published = published

    def __repr__(self):
        return '<Article(id={id}, \
            article_title="{article_title}", \
            article_author="{article_author}", \
            article_category="{article_category}", \
            article_date="{article_date}", \
            article_mod_date="{article_mod_date}", \
            article_text="{article_text}", \
            published="{published}")>'.format(
            id=self.id,
            article_title=self.article_title,
            article_author=self.article_author,
            article_category=self.article_category,
            article_date=self.article_date,
            article_mod_date=self.article_mod_date,
            article_text=self.article_text,
            published=self.published
            )


class Content(sql.Model):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True, nullable=False)
    content_title = sql.Column(String, index=True, unique=True, nullable=False)
    content_author = sql.Column(String, nullable=False)
    content_category = sql.Column(String, nullable=False)
    content_date = sql.Column(String, nullable=False)
    content_text = sql.Column(String, nullable=False)
    published = sql.Column(Integer, nullable=False)

    def __init__(
                self, id, content_title, content_author, content_category,
                content_date, content_text, published):
        self.id = id                     
        self.content_title = content_title
        self.content_author = content_author
        self.content_category = content_category
        self.content_date = content_date
        self.content_text = content_text
        self.published = published

    def __repr__(self):
        return '<Content(id={id}, \
                content_title="{content_title}", \
                content_author="{content_author}", \
                content_category="{content_category}", \
                content_date="{content_date}", \
                content_text="{content_text}", \
                published="{published}")>'.format(
            id=self.id,
            content_title=self.content_title,
            content_author=self.content_author,
            content_category=self.content_category,
            content_date=self.content_date,
            content_text=self.content_text,
            published=self.published
            )


class Categories(sql.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, nullable=False)
    category_title = sql.Column(String, index=True, unique=True, nullable=False)
    category_author = sql.Column(String, nullable=False)
    category_date = sql.Column(String, nullable=False)
    category_desc = sql.Column(String, nullable=False)

    def __init__(self, id, category_title, category_author, 
                category_date, category_desc):
        self.id = id            
        self.category_title = category_title
        self.category_author = category_author
        self.category_date = category_date
        self.category_desc = category_desc

    def __repr__(self):
        return '<Categories(id={id}, \
                category_title="{category_title}", \
                category_author="{category_author}", \
                category_date="{category_date}", \
                category_desc="{category_desc}")>'.format(
            id=self.id,
            category_title=self.category_title,
            category_author=self.category_author,
            category_date=self.category_date,
            category_desc=self.category_desc
            )


class Users(UserMixin, sql.Model):
    __tablename__ = 'registered_users'
    id = Column(Integer, primary_key=True, nullable=False)
    login = sql.Column(String, index=True, nullable=False, unique=True)
    password = sql.Column(String, nullable=False)
    email = sql.Column(String, nullable=False)
    regdate = sql.Column(String, nullable=False)
    usr_level = sql.Column(String, nullable=False)
    
    def __init__(self, id, login, password, email, regdate, usr_level):
        self.id = id
        self.login = login
        self.password = password
        self.email = email
        self.regdate = regdate
        self.usr_level = usr_level

    def __repr__(self):
        return '<Users(id={id}, \
                login="{login}", \
                password="{password}", \
                email="{email}", \
                regdate="{regdate}"), \
                usr_level="{usr_level}")>'.format(
            id=self.id,
            login=self.login,
            password=self.password, 
            email=self.email,
            regdate=self.regdate, 
            usr_level=self.usr_level
            )

    def is_active(self, login):
        if login == Users.query.get(login):
            return Users.query.get(login)

    def is_authenticated(self):
        return True
