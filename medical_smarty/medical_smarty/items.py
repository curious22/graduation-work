import scrapy


class UrlsReporter(scrapy.Item):
    url = scrapy.Field()
