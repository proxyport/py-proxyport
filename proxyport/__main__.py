from .proxyport import ProxyKeeper


for proxy in sorted(ProxyKeeper().get_proxy_list(),
                    key=lambda x: x['country']):
    print('{country} {ip}:{port}'.format(**proxy))
