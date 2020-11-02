from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from furniture_parse import furniture
from furniture_parse.furniture.spiders.houzz_parse import HouzzParseSpider

if __name__ == '__main__':
    crowl_settings = Settings()
    crowl_settings.setmodule(furniture)
    crowl_proc = CrawlerProcess(settings=crowl_settings)

    crowl_proc.crawl(HouzzParseSpider)
    crowl_proc.start()