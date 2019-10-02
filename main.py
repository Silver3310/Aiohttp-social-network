import base64
import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet
from motor.motor_asyncio import AsyncIOMotorClient

from routers.base import setup_routers
from config.common import BaseConfig


def main():
    """
    Run the application
    """
    app = web.Application()

    # Encrypt the cookie for sessions
    # generate a new key
    fernet_key = fernet.Fernet.generate_key()
    # make it safe to use in URLs
    secret_key = base64.urlsafe_b64decode(fernet_key)
    # Now server will remember the browser by cookie
    setup(
        app,
        EncryptedCookieStorage(secret_key)
    )

    # Now the server handles templates
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(
            package_name='main',
            package_path='templates'
        )
    )

    setup_routers(app)
    app['config'] = BaseConfig
    # connect to the db asynchronously (thru motor)
    app['db'] = AsyncIOMotorClient().my_database
    logging.basicConfig(level=logging.DEBUG)  # console level debug
    web.run_app(app)


if __name__ == '__main__':
    main()
