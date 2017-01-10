import pymongo
import settings

connection = pymongo.MongoClient(
    settings.MONGODB_SERVER,
    settings.MONGODB_PORT
)

db = connection[settings.MONGODB_DB]
raw_collection = db[settings.MONGODB_RAW_DATA]
aggregated_collection = db[settings.MONGODB_COLLECTION]
limit = 20


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


def get_item_by_tags(item, source):
    """Generate query by tags and sending the request into DB"""
    tags_list = get_query_from_tags(item['tags'])
    tags_list.append({'source': source})

    coincidence = raw_collection.find_one({'$and': tags_list})

    return coincidence if coincidence else False

raw_count = raw_collection.find({'source': 'add.ua'}).count()

for page in range(1, (raw_count // limit)):
    batch = list(raw_collection.find({'source': 'add.ua'}).skip(limit * page).limit(limit))

    for item in batch:
        coincidence_item = get_item_by_tags(item, 'apteka24.ua')
        if coincidence_item:
            print(
                'id: {}, title: {} url: {}'.format(
                    item['_id'],
                    item['title'],
                    item['price_data'][0]['url']
                )
            )
            print(
                'id: {}, title: {} url: {}'.format(
                    coincidence_item['_id'],
                    coincidence_item['title'],
                    coincidence_item['price_data'][0]['url']
                )
            )
            print('*' * 50)
