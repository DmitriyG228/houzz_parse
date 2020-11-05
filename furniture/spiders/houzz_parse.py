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
        'img_product': '//img[@class="view-product-image__img"]/@src',
    }

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['link_page']):
            yield response.follow(url, callback=self.parse_product_page)

        # Paginator
        url_next_page = response.xpath(self.xpath['next_page']).extract_first()
        yield response.follow(url_next_page, callback=self.parse)

    def parse_product_page(self, response, **kwargs):
        product_variation_json = json.loads(response.xpath('//script[@id="hz-ctx"]/text()').extract_first())
        regex = re.compile(r'^.+\~([0-9]+)')
        product_id = re.findall(regex, response.url)[0]

        # parse product
        loader = FurnitureItem(response=response)
        loader.add_value('url', response.url)
        loader.add_value('product_specifications', product_variation_json)
        loader.add_value('price', product_variation_json['data']['stores']['data']['ProductInfoStore']['data'][product_id]['basePrice'])
        try:
            # Gamma_choise
            gamma_data = product_variation_json['data']['stores']['data']['ProductVariationsStore']['data'][product_id][
                'variationProducts']
            for id, new_gamma_url in gamma_data.items():
                yield response.follow(new_gamma_url['url'], callback=self.parse_product_page)
        except Exception as ex:
            print(f"Can't find gamma")

        try:
            #variation_size_choise
            variation_size = product_variation_json['data']['stores']['data']['ProductVariationsStore']['data'][product_id]['variationsMap']['s']
            variation_map = product_variation_json['data']['stores']['data']['ProductVariationsStore']['data'][product_id]['variationProducts']
            for id, new_variation_url in variation_size.items():

                url_id_str = new_variation_url['spaceId'].__str__()
                yield response.follow(variation_map[url_id_str]['url'], callback=self.parse_product_page)

        except Exception as ex:
            print(f'Can\'t find variation')

        try:
            # Catch IMG
            img_dict_url = {}
            img_ids = product_variation_json['data']['stores']['data']['ProductDataStore']['data'][product_id][
                'imageIds']
            for id_img in img_ids:
                if id_img in img_ids:
                    img_dict_url[
                        id_img] = f'https://st.hzcdn.com/simgs/{id_img}_4-{product_variation_json["data"]["stores"]["data"]["ImageStore"]["data"][id_img]["contentModified"]}/home-design.jpg'
            loader.add_value('url_img_product', img_dict_url)
        except Exception as ex:
            loader.add_xpath('url_img_product', self.xpath['img_product'])

        yield loader.load_item()


