import requests
from furniture import settings


class proxis():

    def __init__(self, url_proxy):
        self.url_proxy_list = url_proxy

    def get_file_proxy(self):
        try:
            request = requests.get(url=self.url_proxy_list)
            if request.status_code == 200:
                with open("../" + settings.ROTATING_proxy_LIST_PATH, 'w+', encoding='utf8') as proxy_list:
                    proxy_list.write(request.text)

        except Exception as ex:
            print(ex)

        print(request.text)


if __name__ == '__main__':
    proxis = proxis('https://proxy.webshare.io/')
    proxis.get_file_proxy()
