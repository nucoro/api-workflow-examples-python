import os
from exceptions import URLNotFound

from .constants import PREFIX_URL
from .urls import urls_pattern


def reverse(url_name, **kwargs):
    ROOT = os.environ.get('BASE_URL')
    url_path = urls_pattern.get(url_name)
    if not url_path:
        raise URLNotFound(f'URL not found: {url_name}')
    url_path = url_path.format(**kwargs)
    return f'{ROOT}{PREFIX_URL}{url_path}'
