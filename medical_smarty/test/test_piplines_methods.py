from medical_smarty.pipelines import MongoDBPipeline

new_item = {
  "source": "add.ua",
  "price_data": [
    {
      "resource": "add.ua",
      "price": 31.94,
      "brand": "Юрия-Фарм ООО (Украина, Киев)",
      "url": "https://www.add.ua/natrija-hlorid-soljuven-0-9-rastvor-dlja-infuzij-200-ml.html",
      "currency": "UAH",
      "availability": True
    }
  ]
}

similar_resource = {
  "source": "add.ua",
  "price_data": [
    {
      "resource": "add.ua",
      "price": 31.94,
      "brand": "Юрия-Фарм ООО (Украина, Киев)",
      "url": "https://www.add.ua/natrija-hlorid-soljuven-0-9-rastvor-dlja-infuzij-200-ml.html",
      "currency": "UAH",
      "availability": True
    },
    {
      "resource": "apteka24.ua",
      "price": 31.94,
      "brand": "Юрия-Фарм ООО (Украина, Киев)",
      "url": "https://www.add.ua/natrija-hlorid-soljuven-0-9-rastvor-dlja-infuzij-200-ml.html",
      "currency": "UAH",
      "availability": True
    }
  ]
}

different_resource = {
  "source": "add.ua",
  "price_data": [
    {
      "resource": "some.com",
      "price": 31.94,
      "brand": "Юрия-Фарм ООО (Украина, Киев)",
      "url": "https://www.add.ua/natrija-hlorid-soljuven-0-9-rastvor-dlja-infuzij-200-ml.html",
      "currency": "UAH",
      "availability": True
    },
    {
      "resource": "apteka24.ua",
      "price": 31.94,
      "brand": "Юрия-Фарм ООО (Украина, Киев)",
      "url": "https://www.add.ua/natrija-hlorid-soljuven-0-9-rastvor-dlja-infuzij-200-ml.html",
      "currency": "UAH",
      "availability": True
    }
  ]
}


def test_get_query_from_tags():
    assert MongoDBPipeline.get_query_from_tags(["гофен", "400", "мг", "капсулы", "№100"]) == \
    [
        {'tags': {'$regex': 'гофен'}},
        {'tags': {'$regex': '400'}},
        {'tags': {'$regex': 'мг'}},
        {'tags': {'$regex': 'капсулы'}},
        {'tags': {'$regex': '№100'}}
    ]


def test_is_similar_resource():
    assert MongoDBPipeline.is_similar_resource(similar_resource, new_item) == True
    assert MongoDBPipeline.is_similar_resource(different_resource, new_item) == False