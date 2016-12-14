import falcon
from search.filter import Filter

api = application = falcon.API()
api.add_route('/api/filter', Filter())
