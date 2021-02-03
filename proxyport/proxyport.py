from datetime import datetime, timedelta
import json
import logging
from random import choice
from urllib.request import urlopen, Request

from .__version__ import __version__

logger = logging.getLogger(__name__)


class ProxyKeeper:
    last_load = None
    api_url = 'https://api.proxy-port.com/public-free'
    user_agent = 'py-proxyport/{}'.format(__version__)
    headers = {'User-Agent': user_agent}

    def __init__(self):
        self.log = logger
        self.proxy_dict = dict()
        self.log.info('proxyport started')

    def set_user_agent(self, user_agent):
        self.headers['User-Agent'] = '{} {}'.format(
            self.user_agent, user_agent)

    def load_proxy(self):
        try:
            response = urlopen(self.get_proxy_list_request())
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

    def get_proxy_list_request(self):
        return Request(self.api_url, headers=self.headers)

    def proxy_list_gc(self):
        now = datetime.now()
        for address, proxy in list(self.proxy_dict.items()):
            if now > proxy['TTL']:
                del self.proxy_dict[address]

    def refresh(self):
        if not self.last_load or \
                self.last_load < datetime.now() - timedelta(seconds=60):
            self.load_proxy()

    def get_random_proxy(self):
        self.refresh()
        if not self.proxy_dict:
            self.log.warning('Proxy list is empty')
        else:
            return 'http://' + choice(list(self.proxy_dict.keys()))

    def get_proxy_list(self):
        self.refresh()
        return self.proxy_dict.values()


keeper = ProxyKeeper()
