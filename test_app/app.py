from bson.json_util import dumps
import falcon
import pymongo


class MongoQueryBlueprint(object):
    """docstring for ."""
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['test-data']
        self.collection = db['processing_status_urls']

    def on_get(self, req, resp):
        completed = self.collection.find({'status': 'COMPLETED'})
        result = list(completed)
        resp.body = dumps(result)
        resp.status = falcon.HTTP_200


api = application = falcon.API()
api.add_route('/completed', MongoQueryBlueprint())
