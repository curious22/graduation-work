import falcon
from bson.json_util import dumps
from search.base import MongoDBConnect, QueryMixin


class Search(MongoDBConnect,
             QueryMixin):
    """
    Implementing search in DB by criteria
    endpoint: /search
    """

    def __init__(self):
        super(Search, self).__init__()

    def on_get(self, req, resp):

        query = req.query_string
        if query:
            conditions, addition = self.query_generation(query)
            page_value = addition.get('page')
            limit_value = addition.get('limit')

            page = int(page_value) if page_value else 0
            limit = int(limit_value )if limit_value else 20

            if conditions:
                data = self.result_generating(
                    self.collection.find({'$and': conditions})
                        .skip(limit * page).limit(limit),
                    page=page,
                    pages=self.get_count_pages(
                        conditions=conditions,
                        limit=limit
                    )
                )
            else:
                data = self.result_generating(
                    self.collection.find().skip(limit * page).limit(limit),
                    page=page,
                    pages=self.get_count_pages(limit=limit)
                )

            resp.body = dumps(data)
            resp.status = falcon.HTTP_200
        else:
            data = self.result_generating(
                self.collection.find().limit(20),
                page=0,
                pages=self.get_count_pages(limit=20)
            )
            resp.body = dumps(data)
            resp.status = falcon.HTTP_200
