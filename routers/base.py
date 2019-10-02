"""
URLs dispatcher
"""
from handlers.base import Index, Login, SignUp


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
