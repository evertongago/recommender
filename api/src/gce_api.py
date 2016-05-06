""" GCE Services API """

import json
import webapp2
import datetime

import src.entity as entity
import src.common.util as util
import src.common.constants as constants

from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import app_identity

CONST = constants.Const()

class Error(Exception):
    """ Error """

class SyncVisitHandler(webapp2.RequestHandler):

    def get(self):
        visits = entity.AccessEntity.query().order(entity.AccessEntity.key).fetch(100)
        csv = ''
        keys = []
        for v in visits:
            timestamp = util.to_timestamp(v.visited_at.timetuple())
            csv += '%s\t%s\t%s\t%s\n' % (v.user_id, v.content_id, v.rate, timestamp)
            keys.append(v.key)

        if not keys:
            return self.response.write(json.dumps({
                "status": CONST.OK,
                "message": "no visits to sync"
            }))

        if len(keys) < 100 and not self.request.get('force'):
            return self.response.write(json.dumps({
                "status": CONST.OK,
                "message": "too few files to sync: %s" % (len(keys))
            }))

        month = datetime.date.today().strftime('%Y%m')
        filename = 'month-%s/visits-%s.txt' % (month, keys[0].id())
        gcs_url = 'http://recommender.storage.googleapis.com/data/visits/%s' % (filename)

        token = util.get_token()
        result =  urlfetch.fetch(gcs_url,
            method=urlfetch.PUT,
            headers={
                'Content-Type': 'text/plain; charset=UTF-8',
                'Authorization': 'Bearer %s' % (token)
            },
            payload=csv
        )

        msg = 'gcs result: %s -- %s' % (result.status_code, result.content)
        if result.status_code != CONST.OK:
            raise Error(msg)

        ndb.delete_multi(keys)
        self.response.write(json.dumps({
                "status": CONST.OK,
                "message": msg
        }))

class StartInstanceHandler(webapp2.RequestHandler):
    def get(self):
        gce_zone = 'us-central1-a'
        gce_machine_type = 'n1-standard-1'
        gce_instance_name = 'recommender'
        gce_image = 'projects/ubuntu-os-cloud/global/images/ubuntu-1404-trusty-v20160406'

        project_id = app_identity.get_application_id()
        token = util.get_token()
        url = 'https://www.googleapis.com/compute/v1/projects/%s/zones/%s/instances' % (project_id, gce_zone)
        opts = {
            'name': gce_instance_name,
            'machineType': 'zones/%s/machineTypes/%s' % (gce_zone, gce_machine_type),
            'disks': [
                {
                    'autoDelete': True,
                    'boot': True,
                    'initializeParams': {
                        'sourceImage': gce_image
                    }
                }
            ],
            'metadata': {
                'items': [
                    {
                        'key': 'startup-script',
                        'value': util.read_file('gce/startup.sh')
                    }
                ]
            },
            'serviceAccounts': [
                {
                    'email': '%s@appspot.gserviceaccount.com' % (project_id),
                    'scopes': util.scopes
                }
            ],
            'networkInterfaces': [
                {
                    'network': 'https://www.googleapis.com/compute/v1/projects/%s/global/networks/default' % (project_id),
                    'accessConfigs': [
                        {
                            'type': 'ONE_TO_ONE_NAT',
                            'name': 'External NAT'
                        }
                    ]
                }
            ]
        }

        result = urlfetch.fetch(url,
            method = urlfetch.POST,
            headers = {
                'Content-Type': 'application/json; charset=UTF-8',
                'Authorization': 'Bearer %s' % (token)
            },
            payload = json.dumps(opts)
        )

        msg = 'Create instance result: %s -- %s' % (result.status_code, result.content)
        if result.status_code != CONST.OK and result.status_code != CONST.NOT_FOUND:
            raise Error(msg)
        else:
            print msg

        self.response.write(json.dumps({
                "status": CONST.OK,
                "message": msg
        }))
