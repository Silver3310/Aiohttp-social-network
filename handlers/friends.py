import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from models.user import User


class FriendsView(web.View):
    """
    Friends View
    """

    @aiohttp_jinja2.template('friends.html')
    async def get(self):
        """Show a list of users"""
        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPForbidden()

        friends = await User.get_user_friends_suggestions(
            db=self.app['db'],
            user_id=session['user']['_id']
        )

        return dict(friends=friends)

    async def post(self):
        return web.HTTPError()
