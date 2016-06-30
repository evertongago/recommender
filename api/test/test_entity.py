import json
import unittest
from src import entity

class EntityTestSuite(unittest.TestCase):

    def test_access_from_json(self):
        access_json = """{
            "id" : 12345,
            "user_id" : 54321,
            "content_id" : "999",
            "rate": 2 
        }"""

        access_map = json.loads(access_json)
        access = entity.AccessEntity.from_dict(access_map)
        self.assertEqual(access.key.id(), 12345)
        self.assertEqual(access.user_id, 54321)
        self.assertEqual(access.content_id, "999")
        self.assertEqual(access.rate, 2)
        self.assertIs(access.validate(), None)

    def test_access_validate_raises_exception(self):
        access_json = """{
            "id" : 12345,
            "user_id" : 54321,
            "rate": 2 
        }"""

        access_map = json.loads(access_json)
        access = entity.AccessEntity.from_dict(access_map)
        self.assertEqual(access.key.id(), 12345)
        self.assertEqual(access.user_id, 54321)
        self.assertIs(access.content_id, None)
        self.assertEqual(access.rate, 2)
        with self.assertRaises(entity.ValidateError):
            access.validate()

    def test_access_to_map(self):
        access = entity.AccessEntity(id=1)
        access.user_id = 2
        access.content_id = "3"
        access.rate = 4
        access_dict = access.to_dict()

        self.assertEqual(access_dict['id'], 1)
        self.assertEqual(access_dict['user_id'], 2)
        self.assertEqual(access_dict['content_id'], "3")
        self.assertEqual(access_dict['rate'], 4)

if __name__ == '__main__':
    unittest.main()       
