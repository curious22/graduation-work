import scrapy
from redis import Redis

from medical_smarty.items import UrlsReporter
from core.helpers import BColors


class AddUaUrls(scrapy.Spider):
    name = 'addua_urls'
    start_urls = [
        'https://www.add.ua/medicamenti/?limit=60'
    ]

    def __init__(self):
        super(AddUaUrls, self).__init__(name=self.name)
        self.redis_client = Redis()
        self.queue = 'addua_processing:start_urls'

    def parse(self, response):
        print(
            BColors.OKBLUE +
            'Parse url: {}'.format(response.url) +
            BColors.ENDC
        )

        if response.xpath('//ul[contains(@class, "products-grid")]'):
            urls = self.get_urls(response)

            if urls:
                self.push_into_redis(urls)
                yield UrlsReporter({'url': response.url})

        # is there are a next page button
        if response.xpath('//a[@class="next i-next"]'):
            url = response.xpath('//a[@class="next i-next"]/@href').extract_first()
            yield scrapy.Request(url, callback=self.parse)

    @staticmethod
    def get_urls(response):
        urls = response.xpath('//p[@class="product-name"]/a/@href').extract()
        return urls

    def push_into_redis(self, list_):
        for url in list_:
            self.redis_client.lpush(self.queue, url)
            print(
                BColors.OKGREEN +
                'URL {} send to {} queue'.format(url, self.queue) +
                BColors.ENDC
            )
