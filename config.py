import os

from version import VERSION


class Config:
    VERSION = VERSION

    SECRET_KEY = os.environ.get('SECRET_KEY', '')

    SPYCLOUD_API_URL = 'https://api.spycloud.io/enterprise-v2/{endpoint}'
