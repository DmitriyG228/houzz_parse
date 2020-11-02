import scrapy


class HouzzParseSpider(scrapy.Spider):
    name = 'houzz_parse'
    allowed_domains = ['www.houzz.com']
    start_urls = ['https://www.houzz.com/products/sofas-and-sectionals']

    xpath = {
        'link_page': '//div[contains(@class, "hz-product-card hz-track-me")]//a[@class="hz-product-card__link"]/@href',
        'next_page': '//a[contains(@class, "hz-pagination-link--next")]/@href',
    }

    xpath_product = {
        'product_specifications': '//d1[contains(@class, "product-specs-group")]',
    }

    def parse(self, response, **kwargs):
        for url in response.xpath(self.xpath['link_page']):
            yield response.follow(url, callback=self.parse_product_page)

        # Paginator
        url_next_page = response.xpath(self.xpath['next_page']).extract_first()
        yield response.follow(url_next_page, callback=self.parse)

    def parse_product_page(self, response, **kwargs):
        print(response)
