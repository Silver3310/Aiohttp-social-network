"""
Views for the application
"""
import hashlib

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from pymongo.results import InsertOneResult

from models.user import User
from models.post import Post


class Index(web.View):
    """
    Index view
    """

    @aiohttp_jinja2.template('index.html')
    async def get(self):  # <Request GET / >
        """Show the introduction for a user"""

        conf = self.app['config']
        session = await get_session(self)
        posts = list()
        friends = list()
        if 'user' in session:
            user = session['user']
            posts = await Post.get_posts_by_user(
                db=self.app['db'],
                user_id=user['_id'],
            )
            friends = await User.get_user_friends(
                db=self.app['db'],
                user_id=user['_id']
            )
        return dict(
            conf=conf,
            posts=posts,
            friends=friends
        )


class Login(web.View):
    """
    Login view
    """

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        """Show the form for entering data"""

        return dict()

    async def post(self):  # <Request POST /login >
        """Singing up"""

        # self.post() is a coroutine object
        data = await self.post()  # take all the data from the form
        email = data['email']
        password = data['password']

        user = await User.get_user(
            db=self.app['db'],
            email=email
        )

        if user.get('error'):
            location = self.app.router['login'].url_for()
            return web.HTTPFound(location=location)

        if user['password'] == hashlib.sha256(
                password.encode('utf-8')
        ).hexdigest():
            session = await get_session(self)
            session['user'] = user

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


class Logout(web.View):
    """
    Logout view
    """

    async def get(self):
        """log out"""
        session = await get_session(self)
        del session['user']

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class PostView(web.View):
    """
    Post handling view
    """

    async def post(self):
        data = await self.post()
        session = await get_session(self)

        if 'user' in session:
            await Post.create_post(
                db=self.app['db'],
                user_id=session['user']['_id'],
                message=data['message']
            )
            return web.HTTPFound(location=self.app.router['index'].url_for())

        return web.HTTPForbidden()
