import pymongo
import settings


class MongoDBConnect(object):
    """Implementing a connecting to MongoDB collection"""

    def __init__(self):
        client = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
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
            if key not in ['page', 'limit']:
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
        }

        return data
