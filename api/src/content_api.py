""" User Content Access API """

import src.entity as entity
import src.common.constants as constants
import webapp2
import json
import uuid as UUID

from Cookie import SimpleCookie

CONST = constants.Const()

class AccessHandler(webapp2.RequestHandler):

    def post(self):
        data = json.loads(self.request.body)
        ent = entity.AccessEntity()

        # get user_id from cookie.
        cookie_name = 'recommender_cookie'
        user_id = self.get_cookie(cookie_name)
        if not user_id:
            uuid = UUID.uuid4()
            user_id = uuid.int
            print('User ID: ', user_id)
            self.add_cookie(cookie_name, user_id)

        ent.user_id = int(data['user_id'])
        ent.content_id = data['content_id']
        ent.rate = int(data['rate'])
        ent.put()

    def get_cookie(self, name):
        cookie_str = self.request.headers.get('cookie')
        if not cookie_str:
            return None
        cookie = SimpleCookie()
        cookie.load(cookie_str)
        return cookie[name].value;

    def add_cookie(self, name, value, path='/', expires=None):
        cookie = SimpleCookie()
        cookie[name] = value
        cookie[name]['path'] = path
        cookie[name]['expires'] = expires
        self.response.headers['Set-Cookie'] = cookie.values()[0].OutputString()

class RecommenderHandler(webapp2.RequestHandler):

    def get(self):
        response_data = {
            "status" : CONST.OK,
            "data" : []
        }

        if not self.request.get('user_id'):
            response_data['status'] = CONST.BAD_REQUEST
            return self.response.write(json.dumps(response_data))

        user_id = int(self.request.get('user_id'))
        if user_id:
            cls = entity.RecommendationContent
            ent = cls.query(cls.user_id == user_id).order(-cls.rate).fetch(20)
            if ent:
                response_data['data'] = [p.to_dict() for p in ent]
            else:
                response_data['status'] = CONST.NOT_FOUND

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(response_data))
