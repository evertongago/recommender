""" User Content Access API """

import src.entity as entity
import src.common.constants as constants
import webapp2
import json

CONST = constants.Const()

class AccessHandler(webapp2.RequestHandler):

    def post(self):
        data = json.loads(self.request.body)
        ent = entity.AccessEntity()
        ent.user_id = int(data['user_id'])
        ent.content_id = data['content_id']
        ent.rate = int(data['rate'])
        ent.put()

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
