from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from furniture import settings
from furniture.spiders.houzz_parse import HouzzParseSpider
from furniture.spiders.houzz_ideas_parse import HouzzIdeasParseSpider
from furniture.proxies import proxis

if __name__ == '__main__':
    #my_proxy = proxis('https://getfreeproxylists.blogspot.com/')

    crowl_settings = Settings()
    crowl_settings.setmodule(settings)
    crowl_proc = CrawlerProcess(settings=crowl_settings)

#    crowl_proc.crawl(HouzzParseSpider)
#    crowl_proc.start()

    crowl_proc.crawl(HouzzIdeasParseSpider)
    crowl_proc.start()