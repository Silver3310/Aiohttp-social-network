import os
from aiohttp import web
from aiohttp_session import get_session

from config.common import BaseConfig
from models.user import User


class Avatar(web.View):
    """
    View for profile pictures of users
    """

    async def post(self):
        """Save avatar"""

        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPForbidden()

        user = session['user']
        data = await self.post()
        avatar = data['avatar']

        avatar_url = os.path.join(
            f'{BaseConfig.STATIC_DIR}/avatars/',
            avatar.filename
        )

        with open(avatar_url, 'wb') as f:
            content = avatar.file.read()
            f.write(content)

        await User.save_avatar_url(
            db=self.app['db'],
            user_id=user['_id'],
            url=f'/avatars/{avatar.filename}'
        )

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)
