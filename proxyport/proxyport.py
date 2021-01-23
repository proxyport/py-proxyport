from datetime import datetime, timedelta
import json
import logging
from random import choice
from urllib.request import urlopen, Request

from .__version__ import __version__

logger = logging.getLogger(__name__)

API_URL = 'https://api.proxy-port.com/public-free'
HEADERS = {'User-Agent': 'py-proxyport/{}'.format(__version__)}


class ProxyKeeper:
    last_load = None

    def __init__(self):
        self.log = logger
        self.proxy_list_request = Request(API_URL, headers=HEADERS)
        self.proxy_dict = dict()
        self.load_proxy()
        self.log.info('proxyport started')

    def load_proxy(self):
        try:
            response = urlopen(self.proxy_list_request)
            proxy_list = json.loads(response.read().decode())
        except Exception as e:
            self.log.error('Error on API call, {}'.format(e))
            return
        ttl = datetime.now() + timedelta(minutes=5)
        for proxy in proxy_list:
            address = '{}:{}'.format(proxy.get('ip'), proxy.get('port'))
            self.proxy_dict[address] = {**proxy, 'TTL': ttl}
        self.log.info(
            'Proxy list loaded, total len: {}'.format(len(self.proxy_dict)))
        self.last_load = datetime.now()
        self.proxy_list_gc()

    def proxy_list_gc(self):
        now = datetime.now()
        for address, proxy in list(self.proxy_dict.items()):
            if now > proxy['TTL']:
                del self.proxy_dict[address]

    def get_random_proxy(self):
        if not self.last_load or \
                self.last_load < datetime.now() - timedelta(seconds=60):
            self.load_proxy()
        if not self.proxy_dict:
            self.log.warning('Proxy list is empty')
        else:
            return 'http://' + choice(list(self.proxy_dict.keys()))

    def get_proxy_list(self):
        return self.proxy_dict.values()


keeper = ProxyKeeper()
