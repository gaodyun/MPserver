#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from mpcode.robot import myrobot
from mpcode.weapis import api
from mpcode.models import db
from werobot.contrib.flask import make_view

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:passwd@127.0.0.1:3306/dbname'

db.init_app(app)
db.create_all(app = app)

app.add_url_rule(
	rule = '/',
	endpoint = 'werobot',
	view_func = make_view(myrobot),
	methods = ['GET', 'POST'],
)

api.init_app(app)

@app.errorhandler(404)
def page_not_found(error):
    return ("anythingyouwant"), 404
