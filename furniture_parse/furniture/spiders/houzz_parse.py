import scrapy
import json
import re
from ..loaders import FurnitureItem


class HouzzParseSpider(scrapy.Spider):
    name = 'houzz_parse'
    allowed_domains = ['www.houzz.com']
    start_urls = ['https://www.houzz.com/products/sofas-and-sectionals']

    xpath = {
        'link_page': '//div[contains(@class, "hz-product-card hz-track-me")]//a[@class="hz-product-card__link"]/@href',
        'next_page': '//a[contains(@class, "hz-pagination-link--next")]/@href',
        'product_specifications': '//d1[contains(@class, "product-specs-group")]',
        'gamma_choises':'',
    }

    xpath_product = {
        'model': '',
        # 'product_ID': '',
        # 'manufactured_By': '',
        # 'sold_By': '',
        # 'size_Weight': '',
        # 'color': '',
        # 'materials': '',
        # 'assembly_Required': '',
        # 'category': '',
        # 'style': '',
        # 'collection': '',

    }

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['link_page']):
            yield response.follow(url, callback=self.parse_product_page)

        # Paginator
        url_next_page = response.xpath(self.xpath['next_page']).extract_first()
        yield response.follow(url_next_page, callback=self.parse)

    def parse_product_page(self, response, **kwargs):
        #Gamma_choise
        product_variation_json = json.loads(response.xpath('//script[@id="hz-ctx"]/text()').extract_first())
        comp = re.compile(r'^.+\~([0-9]+)')
        product_id = re.findall(comp, response.url)[0]
        gamma_data = product_variation_json['data']['stores']['data']['ProductVariationsStore']['data'][product_id]['variationProducts']

        print(gamma_data)
        for id, new_gamma_url in gamma_data.items():
            yield response.follow(new_gamma_url['url'], callback=self.parse_product_page)

        #parse product
        loader = FurnitureItem(response=response)
        for name_param, value in self.xpath:
            loader.add_xpath(name_param, value)

        yield loader.load_item()

        print(response)



