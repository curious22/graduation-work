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

            existing_item = self.is_item_already_exists(
                item['title'],
                item['source']
            )

            if existing_item:
                self.update_item(existing_item, item['price_data'])
                print(
                    BColors.UNDERLINE +
                    "Medicine {} was updated into DB".format(item['title']) +
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

    def is_item_already_exists(self, title, source):
        item = self.collection.find_one(
            {'$and': [
                {'title': title},
                {'source': source}
            ]
             }
        )

        return item['_id'] if item else False

    def update_item(self, _id, new_price_data):
        """
        Updating the field `price_data` of the product
        :param _id: 5857db9b4ad1522dcb9dc76b
        :param new_price_data: list with new data
        :return:
        """
        self.collection.update(
            {
                "_id": _id,
            },
            {
                "$set":
                    {
                        "price_data": new_price_data
                    }
            }
        )
