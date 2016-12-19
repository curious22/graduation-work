# -*- coding: utf-8 -*-
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from core.helpers import BColors


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if 'items' not in spider.name:
            return item

        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            response = self.get_item_by_tags(item)
            resp_list = list(response)

            if resp_list:
                print(len(resp_list))

                # if items have similar resources - skip
                if self.is_similar_resource(item, resp_list[0]):
                    print(
                        BColors.WARNING +
                        'Skip the similar items' +
                        BColors.ENDC
                    )
            else:
                self.collection.insert(dict(item))
                print(
                    BColors.UNDERLINE +
                    "Medicine {} was added into DB".format(item['title']) +
                    BColors.ENDC
                )
        return item

    @staticmethod
    def get_query_from_tags(tags):
        """

        :param tags: ["гофен", "400", "мг", "капсулы", "№100"]
        :return:
        [
            {'tags': {'$regex': 'гофен'}},
            {'tags': {'$regex': '400'}},
            {'tags': {'$regex': 'мг'}},
            {'tags': {'$regex': 'капсулы'}},
            {'tags': {'$regex': '№100'}}
        ]
        """
        query = list()

        for tag in tags:
            query.append(
                {
                    'tags': {
                            '$regex': tag
                    }
                }
            )

        return query

    def get_item_by_tags(self, item):
        """Generate query by tags and sending the request into DB"""
        tags_list = self.get_query_from_tags(item['tags'])
        return self.collection.find({'$and': tags_list})

    @staticmethod
    def is_similar_resource(old_item, new_item):
        """Check entry current resource of item in present prices"""
        old_sources = [
            i['resource'] for i in old_item['price_data']
        ]
        if new_item['source'] in old_sources:
            return True

        return False
