"""
Views for the application
"""
from datetime import datetime

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from pymongo.results import InsertOneResult

from models.user import User


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

        db = self.app['db']
        # user = await User.get_user(uid=1)
        # document = await db.test.find_one()

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

    @aiohttp_jinja2.template('signup.html')
    async def get(self):
        """Show the form for entering data"""

        return dict()

    async def post(self):
        """Singing up a user"""

        data = await self.post()
        result: InsertOneResult = await User.create_new_user(
            db=self.app['db'],
            data=data
        )
        # if result has an attribute 'get' it means that it's a dict and
        # contains an error
        if not result or hasattr(result, 'get'):
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)
