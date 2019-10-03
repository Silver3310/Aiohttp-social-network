import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from models.message import Message


class MessageView(web.View):
    """
    Message view
    """

    @aiohttp_jinja2.template('message.html')
    async def get(self):
        """Get inbox and sent messages"""

        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPForbidden()

        inbox_messages = await Message.get_inbox_messages_by_user(
            db=self.app['db'],
            user_id=session['user']['_id']
        )
        send_messages = await Message.get_send_messages_by_user(
            db=self.app['db'],
            user_id=session['user']['_id']
        )

        return dict(
            inbox_messages=inbox_messages,
            send_messages=send_messages
        )

    async def post(self):
        """Send a message"""

        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPForbidden()

        data = await self.post()
        await Message.create_message(
            db=self.app['db'],
            from_user=session['user']['_id'],
            to_user=data['to_user'],
            message=data['message_text']
        )

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)
