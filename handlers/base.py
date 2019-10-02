"""
Views for the application
"""
from datetime import datetime

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session


class Index(web.View):
    """
    Index view
    """

    @aiohttp_jinja2.template('index.html')
    async def get(self):  # <Request GET / >
        conf = self.app['config']
        return dict(conf=conf)


class Login(web.View):
    """
    Login view
    """

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        """Show the form for entering data"""

        # get_session may take some time
        session = await get_session(self)
        last_visit = session['last_visit'] = str(datetime.now())
        text = f'Last visited: {last_visit}'
        return dict(text=f'login Aiohttp!, {text}')

    async def post(self):  # <Request POST /login >
        """Singing up"""

        # self.post() is a coroutine object
        data = await self.post()  # take all the data from the form
        login = data['login']
        password = data['password']

        # get_session is a coroutine object
        session = await get_session(self)
        session['user'] = {
            'login': login
        }

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)  # 302 moved temporarily


class SignUp(web.View):
    """
    Sign up view
    """

    async def get(self):
        return web.Response(text='signup Aiohttp!')
