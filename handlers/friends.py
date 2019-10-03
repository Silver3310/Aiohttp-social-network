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

        users = await User.get_user_friends_suggestions(
            db=self.app['db'],
            user_id=session['user']['_id']
        )

        return dict(users=users)

    async def post(self):
        """Add a new friend"""

        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPForbidden()

        data = await self.post()
        await User.add_friend(
            db=self.app['db'],
            user_id=session['user']['_id'],
            friend_id=data['uid']
        )
        location = self.app.router['friends'].url_for()
        return web.HTTPFound(location=location)
