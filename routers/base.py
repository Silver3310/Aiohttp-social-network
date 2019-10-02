"""
URLs dispatcher
"""
from handlers.base import Index, Login, SignUp, Logout
from handlers.avatar import Avatar
from config.common import BaseConfig


def setup_routers(app):
    app.router.add_get(
        '/',
        Index.get,
        name='index'
    )
    app.router.add_get(
        '/login',
        Login.get,
        name='login'
    )
    app.router.add_post(
        '/login',
        Login.post
    )
    app.router.add_get(
        '/signup',
        SignUp.get,
        name='signup'
    )
    app.router.add_post(
        '/signup',
        SignUp.post,
        name='signup'
    )
    app.router.add_get(
        '/logout',
        Logout.get,
        name='logout'
    )
    app.router.add_post(
        '/save_avatar',
        Avatar.post,
        name='save_avatar'
    )


def setup_static_routes(app):
    app.router.add_static(
        '/static/',
        path=BaseConfig.STATIC_DIR,
        name='static'
    )
