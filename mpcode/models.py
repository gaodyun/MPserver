#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # wechat user's UnionID
    uid = db.Column(db.String(32), unique = True, nullable = False)
    # the nums of msg
    count = db.Column(db.Integer)
    # if in wish mode, user can send any msg, and sys will not response, 
    # until get over, and only count one time
    # 0 is not in, 1+ is in wish mode
    tag = db.Column(db.Integer)

class System(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # store some key - value => (keyword, value) in sys
    # for example, accesstoken
    keyword = db.Column(db.String(64), unique = True, nullable = False)
    value = db.Column(db.String(1024))
    # this column is for the ttl of keyword, such as the expires time of accesstoken
    ttl = db.Column(db.Integer)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(32), nullable = False)
    description = db.Column(db.String(64), nullable = False)
    # the url of img which in article
    img = db.Column(db.String(128), nullable = False)
    # the url when click article to go
    url = db.Column(db.String(128), nullable = False)
