"""
Views for the application
"""
from datetime import datetime

from aiohttp import web
from aiohttp_session import get_session


class Index(web.View):
    """
    Index view
    """

    async def get(self):
        # conf = self.request.app['config']
        return web.Response(text='Hello Aiohttp!')


class Login(web.View):
    """
    Login view
    """

    async def get(self):
        # get_session may take some time
        session = await get_session(self)
        last_visit = session['last_visit'] = str(datetime.now())
        text = f'Last visited: {last_visit}'
        return web.Response(text=f'login Aiohttp!, {text}')

    async def post(self):
        return web.Response(text='login Aiohttp! POST')


class SignUp(web.View):
    """
    Sign up view
    """

    async def get(self):
        return web.Response(text='signup Aiohttp!')
