import logging

from aiohttp import web

from routers.base import setup_routers


def main():
    """
    Run the application
    """
    app = web.Application()
    setup_routers(app)
    app['config'] = {}
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app)


if __name__ == '__main__':
    main()
