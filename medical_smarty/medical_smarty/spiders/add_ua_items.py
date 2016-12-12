from datetime import datetime

from scrapy_redis.spiders import RedisSpider
from core.helpers import BColors
from core.mixins import Py3RedisSpider
from medical_smarty.items import MedicineItem


class AddUaItems(Py3RedisSpider, RedisSpider):
    name = 'addua_items'

    def parse(self, response):
        current_time = datetime.now().strftime('%H:%M:%S %d-%m-%y')
        print(
            BColors.OKBLUE +
            '{} Processing record at {}'.format(current_time, response.url) +
            BColors.ENDC
        )

        metadata = self.get_metadata_html(response)
        yield MedicineItem(**metadata)

    @staticmethod
    def get_metadata_html(response):
        """Obtaining metadata from response HTML page"""
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
            ).extract_first(),
            'source': 'add.ua'
        }

        if response.xpath('//p[@class="availability in-stock"]'):
            metadata['availability'] = True
        elif response.xpath(
                '//p[contains(@class, "availability out-of-stock")]'
        ):
            metadata['availability'] = False

        # tag generation
        metadata['tags'] = metadata['title'].lower().split()

        # get category
        category = response.xpath(
            '//div[@class="breadcrumbs"]/ul/a/span/text()'
        ).extract()[-1]
        metadata['category'] = category.strip()

        return metadata
