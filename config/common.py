"""
Common config for the application
"""
from .secret import SECRET_KEY


class BaseConfig:

    debug = True
    app_name = 'Social Network'
    secret_key = SECRET_KEY
    database_name = 'my_database'
    static_dir = '/home/alexey/Documents/projects/async_web/social_network/static'

