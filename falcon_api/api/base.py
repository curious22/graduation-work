from urllib.parse import unquote
import pymongo
from pymongo.errors import ServerSelectionTimeoutError
import settings


class MongoDBConnect(object):
    """Implementing a connecting to MongoDB collection"""

    def __init__(self):
        try:
            client = pymongo.MongoClient(
                settings.MONGODB_SERVER,
                settings.MONGODB_PORT,
                serverSelectionTimeoutMS=1
            )
            client.server_info()
        except ServerSelectionTimeoutError as error:
            print(error)
        else:
            db = client[settings.MONGODB_DB]
            self.collection = db[settings.MONGODB_COLLECTION]


class QueryMixin(object):
    """
    Implementing work for obtaining query's criteria
    and result's generating
    """

    @staticmethod
    def query_generation(req_str):
        query = req_str.split('&')
        data = list()
        addition = dict()

        for criterion in query:
            key, value = criterion.split('=')

            #  'page' and 'limit' don't participate in the query
            if key not in ['page', 'limit']:
                if value in ['true', 'false']:
                    value = True if value == 'true' else False

                # title looking in tags
                if key == 'title':
                    list_ = unquote(value).lower().split()

                    for word in list_:
                        data.append(
                            {
                                'tags': word
                            }
                        )
                    else:
                        continue

                # title looking by regex
                if key == 'category':
                    list_ = unquote(value).lower().split()

                    for word in list_:
                        data.append(
                            {
                                'category': {
                                    '$regex': word,
                                    '$options': 'i'
                                }
                            }
                        )
                    else:
                        continue

                data.append(
                    {
                        key: value
                    }
                )
            else:
                addition[key] = value

        return data, addition

    @staticmethod
    def result_generating(cursor, *args, **kwargs):
        result = list(cursor)

        data = {
            'count': len(result),
            'results': result,
            'page': kwargs.get('page'),
            'pages': kwargs.get('pages'),
        }

        return data

    def get_count_pages(self, *args, **kwargs):
        conditions = kwargs.get('conditions')
        limit = kwargs.get('limit')

        if conditions:
            pages = self.collection.find({'$and': conditions}).count() // limit
        else:
            pages = self.collection.find().count() // limit

        return pages
