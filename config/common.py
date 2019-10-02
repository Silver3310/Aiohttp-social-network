"""
Common config for the application
"""
import pathlib

from .secret import SECRET_KEY


class BaseConfig:

    debug = True
    app_name = 'Social Network'
    secret_key = SECRET_KEY
    database_name = 'my_database'

    PROJECT_ROOT = pathlib.Path(__file__).parent.parent
    STATIC_DIR = str(PROJECT_ROOT / 'static')

