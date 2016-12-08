from scrapy_redis.spiders import RedisSpider
from core.helpers import BColors
from medical_smarty.items import MedicineItem


class AddUaItems(RedisSpider):
    name = 'addua_items'
    # redis_key = 'addua_items:start_urls'

    def parse(self, response):
        print(
            BColors.OKBLUE +
            'Processing record at {}'.format(response.url) +
            BColors.ENDC
        )

        metadata = {
            'title': response.xpath(
                '//meta[@property="og:title"]/@content'
            ).extract_first(),
            'url': response.url,
            'price': float(
                response.xpath(
                    '//meta[@property="product:price:amount"]/@content'
                ).extract_first()
            ),
            'currency': response.xpath(
                '//meta[@property="product:price:currency"]/@content'
            ).extract_first(),
            'image_url': response.xpath(
                '//meta[@property="og:image"]/@content'
            ).extract_first(),
            'brand': response.xpath(
                '//meta[@property="og:brand"]/@content'
            ).extract_first()
        }

        yield MedicineItem(**metadata)
