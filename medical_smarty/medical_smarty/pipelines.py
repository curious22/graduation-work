# -*- coding: utf-8 -*-
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from core.helpers import BColors
from bson.objectid import ObjectId


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

                # if items have similar resources - skip
                if self.is_similar_resource(resp_list[0], item):
                    print(
                        BColors.WARNING +
                        'Skip the similar items' +
                        BColors.ENDC
                    )
                else:
                    id_ = resp_list[0]['_id']
                    price_data = self.preparing_new_price_data(
                        item,
                        resp_list[0]
                    )
                    self.update_item(id_, price_data)
                    print(
                        BColors.OKGREEN +
                        'Item {} was updated'.format(item['title']) +
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

    def update_item(self, id_, new_price_data):
        """
        Updating the field `price_data` of the product
        :param id_: 5857db9b4ad1522dcb9dc76b
        :param new_price_data: list with new data
        :return:
        """
        self.collection.update(
            {
                "_id": id_,
            },
            {
                "$set":
                    {
                        "price_data": new_price_data
                    }
            }
        )

    @staticmethod
    def get_price_data(item):
        return item['price_data']

    def preparing_new_price_data(self, new_item, old_item):
        """Creating new `price_data` by combining"""

        price_data = self.get_price_data(old_item)
        new_price_data = self.get_price_data(new_item)

        price_data.append(new_price_data[0])

        return price_data
