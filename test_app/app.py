from bson.json_util import dumps
import falcon
import pymongo


class BaseMongo(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client['test-data']
        self.collection = db['processing_status_urls']
        self.allowed_status = ['completed', 'skipped']


class CheckStatus(BaseMongo):
    def __init__(self):
        super(CheckStatus, self).__init__()

    def on_get(self, req, resp):
        if req.query_string not in self.allowed_status:
            raise falcon.HTTPBadRequest("Requested status doesn't support")

        status = req.query_string
        completed = self.collection.find({'status': status.upper()})
        result = list(completed)
        data = {
            'status': status,
            'count': len(result),
            'results': result
        }
        resp.body = dumps(data)
        resp.status = falcon.HTTP_200

api = application = falcon.API()
api.add_route('/status', CheckStatus())
