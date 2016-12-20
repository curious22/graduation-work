import scrapy
from urllib.parse import urljoin
from core.helpers import print_current_time


class Apteka24Items(scrapy.Spider):
    name = 'apteka24_items'

    start_urls = [
        'http://www.apteka24.ua/gofen-200-kaps-myag-200mg-n60-10kh6-/',
        'http://www.apteka24.ua/metformin-sandoz-tabletki-500mg-n120/',
    ]

    def parse(self, response):
        print_current_time(response)

        metadata = self.get_metadata_html(response)
        return

    @staticmethod
    def get_metadata_html(response):
        """Obtaining metadata from response HTML page"""
        price_data = list()

        img_url = response.xpath(
            '//div[@class="goods_page_slider"]//div[@class="item"]/img/@src'
        ).extract_first()

        metadata = dict(
            title=response.xpath('//h1[@class="title"]/text()').extract_first(),
            image_url=urljoin(response.url, img_url),
            source='apteka24.ua',
        )

        price_data_dict = dict(
            url=response.url,
            resource='add.ua',

        )
