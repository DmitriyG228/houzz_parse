from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from furniture import settings
from furniture.spiders.houzz_parse import HouzzParseSpider

if __name__ == '__main__':
    crowl_settings = Settings()
    crowl_settings.setmodule(settings)
    crowl_proc = CrawlerProcess(settings=crowl_settings)

    crowl_proc.crawl(HouzzParseSpider)
    crowl_proc.start()