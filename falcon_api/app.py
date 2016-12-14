import falcon
from api import search

api = application = falcon.API()
api.add_route('/api/search', search.Search())
