import httplib2
import re

from pathlib import Path
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from urllib.parse import urlparse

from .items import FurnitureItem, DesignItem

def get_product_spec(item):
    current_id = str(item[0]['data']['stores']['data']['ProductDataStore']['data']['currentSpaceId'])
    params_json = item[0]['data']['stores']['data']['ProductDataStore']['data'][current_id]
    array_params_json = {}
    for id, data_params in params_json['productSpec']['productSpecItems'].items():
        array_params_json[data_params['name']] = data_params['value']
    return array_params_json

def get_img(url, name, path):
    h = httplib2.Http()
    response, content = h.request(url)
    path = f'/home/dima/ssd/furniture_data/pictures'
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(f'{path}/{name}.jpg', 'wb') as out:
        out.write(content)
    # h.delete('.cache')

def catch_name(url):
    url_parse = urlparse(url)
    try:
        #https://st.hzcdn.com/simgs/0621936e0932aa0d_9-2506/home-design.jpg
        regex = re.compile(r'\/simgs\/([0-9A-Za-z_\-]+)\/.+')
        name_file = re.findall(regex, url_parse.path)[0]
    except Exception:
        print(f'Can\'t regex: {regex}')

        try:
            #https://st.hzcdn.com/simgs/pictures/closets/formal-mediterranean-paradise-valley-argue-custom-homes-img~78810f760e978814_9-5671-1-9cb82af.jpg
            regex = re.compile(r'\/simgs\/.+\~([0-9A-Za-z_\-]+)\/.+')
            name_file = re.findall(regex, url_parse.path)[0]
        except Exception:
            print(f'Can\'t regex: {regex}')

            name_file = None

    return name_file

def load_img(item):
    if isinstance(item, list):
        for id, url in item[0].items():
            get_img(url, catch_name(url), path=f'./PICTURE')
    else:
        get_img(item[0], catch_name(item[0]), path=f'./PICTURE')

    return item

def load_one_img(item):
    get_img(item[0], catch_name(item[0]), path=f'./PICTURE_DISIGN')

    return item



class FurnitureItem(ItemLoader):
    default_item_class = FurnitureItem

    product_specifications_in = get_product_spec
    url_img_product_in = load_img

    url_out = TakeFirst()
    product_specifications_out = TakeFirst()
    url_img_product_out = TakeFirst()
    price_out = TakeFirst()

class DesignItem(ItemLoader):
    default_item_class = DesignItem

    photo_url_in = load_one_img

    url_out = TakeFirst()
    type_place_out = TakeFirst()
    image_data_out = TakeFirst()
    photo_url_out = TakeFirst()