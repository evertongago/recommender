import time
import os
import StringIO

from datetime import datetime
from google.appengine.api import app_identity

scopes = [
    'https://www.googleapis.com/auth/devstorage.read_write',
    'https://www.googleapis.com/auth/compute',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/datastore',
    'https://www.googleapis.com/auth/userinfo.email'
]

def get_token():
    ret, _ = app_identity.get_access_token(scopes)
    return ret

def to_timestamp(timetuple):
    timestamp = time.mktime(timetuple)
    return int(timestamp)

def read_file(filename):
    folder = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r') as f:
        return f.read().strip()
