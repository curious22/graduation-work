import scrapy


class UrlsReporter(scrapy.Item):
    url = scrapy.Field()


class MedicineItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    image_url = scrapy.Field()
    brand = scrapy.Field()
