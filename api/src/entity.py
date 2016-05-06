""" GAE Datastore entities definition """

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

class Error(Exception):
    """ Error """


class ValidateError(Exception):
    """ Error """


def require(obj, field):
    if getattr(obj, field) is None:
        raise ValidateError('field is required: %s' % (field))


class _Model(ndb.Model):

    @classmethod
    def from_dict(cls, json):
        model = cls(id=json['id'])
        for key, value in json.iteritems():
            if key != 'id':
                setattr(model, key, value)
        return model

    def to_dict(self):
        dictionary = {}

        for prop in self._properties:
            value = getattr(self, prop)
            if value:
                dictionary[prop] = _Model.__from_type_to_raw_value(self._properties[prop], value)

        if 'id' in dir(self.key):
            dictionary['id'] = self.key.id()

        return dictionary

    # todo: parse StructuredProperty
    @classmethod
    def __from_type_to_raw_value(cls, field, value):
        types = {'StringProperty': cls.__decode_str, 'IntegerProperty': cls.__to_int,
                 'DateTimeProperty': cls._convert_date, 'BooleanProperty': bool,
                 'TextProperty': cls.__decode_str}

        field_type = type(field).__name__
        return types[field_type](value) if field_type in types else None

    @classmethod
    def __decode_str(cls, value):
        if isinstance(value, unicode):
            return value.encode('utf8')
        return value

    @classmethod
    def __to_int(self, value):
        if not value:
            return 0
        return int(value)

    @classmethod
    def _convert_date(cls, date):
        if type(date) == datetime:
            return moment.date(date).strftime('%Y-%m-%d')
        else:
            return cls._str_to_date(date)

    @classmethod
    def _str_to_date(cls, input):
        if not data:
            return None
        date_parts = data.split('/')
        date = (datetime(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])))
        return date

    def validate(self):
        """ ok """

class AccessEntity(_Model):
    user_id = ndb.IntegerProperty(indexed=False)
    content_id = ndb.StringProperty(indexed=True)
    rate = ndb.IntegerProperty(indexed=False)
    visited_at = ndb.DateTimeProperty(auto_now_add=True)

    def validate(self):
        require(self, 'user_id')
        require(self, 'content_id')
        require(self, 'rate')

class RecommendationContent(_Model):
    user_id = ndb.IntegerProperty(indexed=True)
    content_id = ndb.StringProperty(indexed=False)
    rate = ndb.FloatProperty(indexed=True)
