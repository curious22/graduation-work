import falcon
from search.search import Search

api = application = falcon.API()
api.add_route('/search', Search())
