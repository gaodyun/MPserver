#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from flask import request
from flask_restplus import Api, Resource
from models import db, User, System, Article

weapistoken = "yourapitoken"

api = Api(doc = False)

def apiauth(func):
    def wrapper(*args, **kwargs):
        if (kwargs['weapitoken'] == weapistoken):
            return func(*args, **kwargs)
        else:
            return {'code': '403'}
    return wrapper

@api.route('/weapis/system/<string:weapitoken>')
class SystemApi(Resource):

    @apiauth
    def get(self, weapitoken):
        sys = System.query.filter_by(keyword = request.args.get('keyword')).first()
        if sys is None:
            return {'keyword': 'null', 'value': 0, 'ttl': 0}
        return {'keyword': sys.keyword, 'value': sys.value, 'ttl': sys.ttl}

    @apiauth
    def post(self, weapitoken):
        r = request.get_json()
        sys = System(keyword = r['keyword'] , value = r['value'], ttl = r['ttl'])
        db.session.add(sys)
        db.session.commit()
        return {'keyword': sys.keyword, 'value': sys.value, 'ttl': sys.ttl}

    @apiauth
    def put(self, weapitoken):
        r = request.get_json()
        sys = System.query.filter_by(keyword = r['keyword']).first()
        sys.value = r['value']
        sys.ttl = r['ttl']
        db.session.commit()
        return {'keyword': sys.keyword, 'value': sys.value, 'ttl': sys.ttl}

@api.route('/weapis/user/<string:weapitoken>')
class UserApi(Resource):

    @apiauth
    def get(self, weapitoken):
        user = User.query.filter_by(uid = request.args.get('uid')).first()
        if user is None:
            return {'uid': 'null', 'count': 0, 'tag': 0}
        return {'uid': user.uid, 'count': user.count, 'tag': user.tag}

    @apiauth
    def post(self, weapitoken):
        r = request.get_json()
        user = User(uid = r['uid'], count = 0, tag = 0)
        db.session.add(user)
        db.session.commit()
        return {'uid': user.uid, 'count': user.count, 'tag': user.tag}

    @apiauth
    def put(self, weapitoken):
        r = request.get_json()
        user = User.query.filter_by(uid = r['uid']).first()
        user.count = r['count']
        user.tag = r['tag']
        db.session.commit()
        return {'uid': user.uid, 'count': user.count, 'tag': user.tag}

    @apiauth
    def delete(self, weapitoken):
	r = request.get_json()
        user = User.query.filter_by(uid = r['uid']).first()
	db.session.delete(user)
	db.session.commit()
	return {'code': 200}
        
@api.route('/weapis/article/<string:weapitoken>')
class ArticleApi(Resource):
    
    @apiauth
    def get(self, weapitoken):
        nums = Article.query.count()
        if (nums == 0):
            return {"title": "null"}
        while (True):
	    aid = random.randint(1, nums)
            article = Article.query.filter_by(id = aid).first()
	    if (article != None):
        	return {'title': article.title, 'description': article.description, 'img': article.img, 'url': article.url}

    @apiauth
    def post(self, weapitoken):
        r = request.get_json()
        article = Article(title = r['title'], description = r['description'], img = r['img'], url = r['url'])
        db.session.add(article)
        db.session.commit()
        return {'title': article.title, 'description': article.description, 'img': article.img, 'url': article.url}
