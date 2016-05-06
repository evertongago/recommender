""" webapp2 routes """

import src.content_api as content_api
import src.gce_api as gce_api
import webapp2
import os

class PingService(webapp2.RequestHandler):

    """ Health check API """

    def get(self):

        self.response.body = 'ping_service'

APP = webapp2.WSGIApplication([
    ('/api/ping', PingService),
    ('/api/content/access', content_api.AccessHandler),
    ('/api/content/recommender', content_api.RecommenderHandler),
    ('/api/sync', gce_api.SyncVisitHandler),
    ('/api/run', gce_api.StartInstanceHandler)
])
