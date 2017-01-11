import pymongo
import settings
import pprint

connection = pymongo.MongoClient(
    settings.MONGODB_SERVER,
    settings.MONGODB_PORT
)

db = connection[settings.MONGODB_DB]
raw_collection = db[settings.MONGODB_RAW_DATA]
aggregated_collection = db[settings.MONGODB_COLLECTION]
limit = 20
set_of_coincidence = set()


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


def print_item_info(item_dict):
    print(
        'id: {}, title: {} url: {}'.format(
            item_dict['_id'],
            item_dict['title'],
            item_dict['price_data'][0]['url']
        )
    )


def get_image_url(item_one, item_two):
    image_url_one = item_one['image_url']
    image_url_two = item_two['image_url']

    image_url = ''

    if not 'No_Picture' in image_url_one:
        image_url = image_url_one
    elif not 'no-image' in image_url_two:
        image_url = image_url_two
    else:
        image_url = image_url_two

    return image_url


def create_new_item(item_one, item_two):
    price_data = item_one['price_data']
    price_data.append(item_two['price_data'][0])

    image_url = get_image_url(item_one, item_two)

    new_item = {
        'title': item_one['title'],
        'category': item_one['category'],
        'image_url': image_url,
        'tags': item['tags'],
        'price_data': price_data
    }

    return new_item

# processing similar goods
raw_count = raw_collection.find({'source': 'add.ua'}).count()

for page in range(1, (raw_count // limit)):
    batch = list(raw_collection.find({'source': 'add.ua'})
                 .skip(limit * page).limit(limit))

    for item in batch:
        coincidence_item = get_item_by_tags(item, 'apteka24.ua')
        if coincidence_item:
            new_item = create_new_item(item, coincidence_item)

            print_item_info(item)
            print_item_info(coincidence_item)

            aggregated_collection.insert(new_item)

            set_of_coincidence.add(item['_id'])
            set_of_coincidence.add(coincidence_item['_id'])

print(len(set_of_coincidence))

# processing other goods
raw_count = raw_collection.find().count()

for page in range(1, (raw_count // limit)):
    batch = list(raw_collection.find().skip(limit * page).limit(limit))

    for item in batch:
        if item['_id'] not in set_of_coincidence:
            item.pop('_id')
            item.pop('source')

            aggregated_collection.insert(item)
