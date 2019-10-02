import base64
import logging

from aiohttp import web
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

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

    setup_routers(app)
    app['config'] = BaseConfig
    logging.basicConfig(level=logging.DEBUG)  # console level debug
    web.run_app(app)


if __name__ == '__main__':
    main()
