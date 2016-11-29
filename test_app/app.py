from bson.json_util import dumps
import falcon
import pymongo


class BaseMongo(object):
    """docstring for ."""
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['test-data']
        self.collection = db['processing_status_urls']


class Completed(BaseMongo):
    """docstring for ."""
    def __init__(self):
        super(Completed, self).__init__()

    def on_get(self, req, resp):
        completed = self.collection.find({'status': 'COMPLETED'})
        result = list(completed)
        data = {
            'count': len(result),
            'results': result
        }
        resp.body = dumps(data)
        resp.status = falcon.HTTP_200

class Skipped(BaseMongo):
    """docstring for ."""
    def __init__(self):
        super(Skipped, self).__init__()

    def on_get(self, req, resp):
        completed = self.collection.find({'status': 'SKIPPED'})
        result = list(completed)
        data = {
            'count': len(result),
            'results': result
        }
        resp.body = dumps(data)
        resp.status = falcon.HTTP_200


api = application = falcon.API()
api.add_route('/completed', Completed())
api.add_route('/skipped', Skipped())
