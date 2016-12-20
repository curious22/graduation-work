import scrapy
from redis import Redis
from urllib.parse import urljoin

from medical_smarty.items import UrlsReporter
from core.mixins import RedisQueueMixin


class Apteka24Urls(RedisQueueMixin ,scrapy.Spider):
    name = 'apteka24_urls'
    start_urls = [
        'http://www.apteka24.ua/'
    ]

    def __init__(self):
        super(Apteka24Urls, self).__init__(name=self.name)
        self.redis_client = Redis()
        self.queue = 'apteka24_items:start_urls'

    def parse(self, response):
        categories = response.xpath(
            '//li[contains(./a/@href, "/medikamenty/")]'
            '/div[@class="nav_second clearfix"]/ul/li/a/@href'
        ).extract()

        for category in categories:
            yield scrapy.Request(
                url=urljoin(response.url, category),
                callback=self.parse_category
            )

    def parse_category(self, response):
        if response.xpath('//div[@class="main_cont"]'):
            urls = self.get_urls(response)
            self.push_into_redis(urls)
            yield UrlsReporter({'url': response.url})

        if response.xpath('//li[@class="next"]'):
            next_page_url = response.xpath(
                '//li[@class="next"]/a/@href'
            ).extract_first()
            yield scrapy.Request(
                url=urljoin(response.url, next_page_url),
                callback=self.parse_category
            )

    @staticmethod
    def get_urls(response):
        urls = response.xpath(
            '//div[@class="main_cont"]//ul[@class="list_view"]/li/a/@href'
        ).extract()

        urls = [urljoin(response.url, i) for i in urls]

        return urls
