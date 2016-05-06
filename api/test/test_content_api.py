import webapp2
import json

from src import main
import src.entity as entity
import src.common.constants as constants
import test.common.test_common as test_common

CONST = constants.Const()

class AccessHandlerTestSuite(test_common.CommonHandlerTest):

    def test_content_access(self):
        request = webapp2.Request.blank('/api/content/access')
        request.method = 'POST'
        request.headers['Content-Type'] = 'application/json'
        request.body = """{
            "user_id" : "1",
            "content_id" : "15",
            "rate" : "5"
        }"""
        response = request.get_response(main.APP)
        self.assertEqual(response.status_int, CONST.OK)

    def test_content_recommender_bad_request(self):
        request = webapp2.Request.blank('/api/content/recommender')
        request.method = 'GET'
        response = request.get_response(main.APP)
        data = json.loads(response.body)
        self.assertEqual(data['status'], CONST.BAD_REQUEST)

    def test_content_recommender_invalid_user(self):
        request = webapp2.Request.blank('/api/content/recommender?user_id=1')
        request.method = 'GET'
        response = request.get_response(main.APP)
        data = json.loads(response.body)
        self.assertEqual(data['status'], CONST.NOT_FOUND)

    def test_content_recommender_ok(self):
        ent = entity.RecommendationContent()
        ent.user_id = int(1)
        ent.content_id = "15"
        ent.rate = int(10)
        ent.put()

        request = webapp2.Request.blank('/api/content/recommender?user_id=1')
        request.method = 'GET'
        response = request.get_response(main.APP)
        data = json.loads(response.body)
        self.assertEqual(data['status'], CONST.OK)
