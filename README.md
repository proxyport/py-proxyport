
# Proxy Port SDK
Proxyport is a Python package that provides interfaces to the [Proxy Port](https://proxy-port.com) API.
## Installation
Install via [pip](https://pip.pypa.io/):
```shell
$ pip install proxyport
```
## Getting Started
Package can be used as module:
```shell
$ python -m proxyport

AR 181.119.301.272:3128
...
UA 194.242.310.289:3128
US 162.144.277.318:3838

```

Example:
```python
from proxyport import get_random_proxy

print(get_random_proxy())

http://139.180.281.313:3128
```
