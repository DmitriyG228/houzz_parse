from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

from .items import FurnitureItem

class HhAutoLoader(ItemLoader):
    default_item_class = FurnitureItem

    url_out = TakeFirst()
