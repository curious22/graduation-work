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
        price_data = []

        metadata = {
            'title': response.xpath(
                '//meta[@property="og:title"]/@content'
            ).extract_first(),

            'image_url': response.xpath(
                '//meta[@property="og:image"]/@content'
            ).extract_first(),

            'source': 'add.ua'
        }

        price_data_dict = {
            'url': response.url,
            'price': float(
                response.xpath(
                    '//meta[@property="product:price:amount"]/@content'
                ).extract_first()
            ),
            'currency': response.xpath(
                '//meta[@property="product:price:currency"]/@content'
            ).extract_first(),
            'brand': response.xpath(
                '//meta[@property="og:brand"]/@content'
            ).extract_first(),
        }

        if response.xpath('//p[@class="availability in-stock"]'):
            price_data_dict['availability'] = True
        elif response.xpath(
                '//p[contains(@class, "availability out-of-stock")]'
        ):
            price_data_dict['availability'] = False

        # tag generation
        metadata['tags'] = metadata['title'].lower().split()

        # get category
        category = response.xpath(
            '//div[@class="breadcrumbs"]/ul/a/span/text()'
        ).extract()[-1]
        metadata['category'] = category.strip()

        price_data.append(price_data_dict)
        metadata['price_data'] = price_data

        return metadata
