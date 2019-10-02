"""
Common config for the application
"""
from .secret import SECRET_KEY


class BaseConfig:

    debug = True
    app_name = 'Social Network'
    secret_key = SECRET_KEY
