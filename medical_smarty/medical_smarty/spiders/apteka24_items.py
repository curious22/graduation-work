from scrapy_redis.spiders import RedisSpider
from core.mixins import Py3RedisSpider
from urllib.parse import urljoin
from core.helpers import print_current_time, get_correct_tags
from medical_smarty.items import MedicineItem


class Apteka24Items(Py3RedisSpider, RedisSpider):
    name = 'apteka24_items'

    def parse(self, response):
        print_current_time(response)

        metadata = self.get_metadata_html(response)

        return MedicineItem(**metadata)

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
            price=float(response.xpath(
                '//div[@class="price"]/@content'
            ).extract_first()),
            currency=response.xpath(
                '//meta[@itemprop="priceCurrency"]/@content'
            ).extract_first(),
            barnd=response.xpath(
                '//li[./span[@class="icon manufacture"]]'
                '/span[@class="count"]/text()'
            ).extract_first(),
        )

        availability = response.xpath(
            '//link[@itemprop="availability"]/@href'
        ).extract_first()

        if 'InStock' in availability:
            price_data_dict['availability'] = True
        else:
            price_data_dict['availability'] = False

        category = response.xpath(
            '//div[@class="breadcrumbs wrapper"]//span/text()'
        ).extract()
        metadata['category'] = category[1]

        price_data.append(price_data_dict)
        metadata['price_data'] = price_data

        return metadata

    @staticmethod
    def custom_title_splitter(tags):
        new_list = list()

        for tag in tags:
            new_tags_list = get_correct_tags(tag)

            for i in new_tags_list:
                new_list.append(i)

        return new_list

