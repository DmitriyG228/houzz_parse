import scrapy
import json
import re
from ..loaders import FurnitureItem, DesignItem


class HouzzIdeasParseSpider(scrapy.Spider):
    name = 'houzz_ideas_parse'
    allowed_domains = ['www.houzz.com']
    start_urls = ['https://www.houzz.com/photos/home-design-ideas-phbr0-bp~']

    xpath = {
        'category': '//a[@data-compid="topCategory"]/@href',
        'ideas_page': '//div[contains=(@class, "hz-space-card__image-container")/@href',
        'next_page': '//div[@class="hz-pagination-link hz-pagination-link--next"]/@href',
    }

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['category']):
            regex = re.compile(r'^.+\_([0-9]+)$')
            category_id = re.findall(regex, url.get())[0]
            name_category = response.xpath(f'//a[@data-compid="topCategory" and contains(@href, "{category_id}")]//div[contains(@class, "category-card__name")]//text()').extract_first()
            yield response.follow(url, callback=self.parse_category, cb_kwargs={'name_category': name_category})

    def parse_category(self, response, **kwargs):

        data_category_json = json.loads(response.xpath('//script[@id="hz-ctx"]/text()').extract_first())
        category_list = data_category_json['data']['stores']['data']['SpaceStore']['data']
        try:
            for id, data in category_list.items():
                cb_kwargs = {
                    'name_category': kwargs['name_category'],
                    'image_data': data,
                }
                yield response.follow(data['url'], callback=self.parse_ideas_page, cb_kwargs=cb_kwargs)
        except Exception as ex:
            print(f'category_list is NULL, :url {response.url}')

        #paginator on category
        url_next = response.xpath(self.xpath['next_page'])
        yield response.follow(url_next, callback=self.parse_category, cb_kwargs={'name_category': kwargs['name_category']})



    def parse_ideas_page(self, response, **kwargs):

        # parse product
        loader = DesignItem(response=response)
        loader.add_value('url', response.url)
        loader.add_value('type_place_out', kwargs['name_category'])
        loader.add_value('image_data', kwargs['image_data'])
        yield loader.load_item()


