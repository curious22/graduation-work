import falcon
from falcon_cors import CORS
from api import search

cors = CORS()
api = application = falcon.API(middleware=[cors.middleware])
api.add_route('/api/search', search.Search())
