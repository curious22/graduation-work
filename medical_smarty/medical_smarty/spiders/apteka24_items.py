import scrapy
from urllib.parse import urljoin
from core.helpers import print_current_time, correct_wrong_designation


class Apteka24Items(scrapy.Spider):
    name = 'apteka24_items'

    start_urls = [
        'http://www.apteka24.ua/gofen-200-kaps-myag-200mg-n60-10kh6-/',
        'http://www.apteka24.ua/metformin-sandoz-tabletki-500mg-n120/',
    ]

    def parse(self, response):
        print_current_time(response)

        metadata = self.get_metadata_html(response)
        from pprint import pprint
        pprint(metadata)
        return

    def get_metadata_html(self, response):
        """Obtaining metadata from response HTML page"""
        price_data = list()

        title = response.xpath('//h1[@class="title"]/text()').extract_first()

        img_url = response.xpath(
            '//div[@class="goods_page_slider"]//div[@class="item"]/img/@src'
        ).extract_first()

        metadata = dict(
            title=title,
            image_url=urljoin(response.url, img_url),
            source='apteka24.ua',
            tags=self.custom_title_splitter(
                title.lower().split()
            )
        )

        price_data_dict = dict(
            url=response.url,
            resource='apteka24.ua',

        )

        price_data.append(price_data_dict)
        metadata['price_data'] = price_data

        return metadata

    @staticmethod
    def custom_title_splitter(list_):
        new_list = list()

        for word in list_:
            item = correct_wrong_designation(word)

            if item and isinstance(item, list):
                for i in item:
                    new_list.append(i)
                continue

            if item:
                new_list.append(item)
                continue

            new_list.append(word)

        return new_list

