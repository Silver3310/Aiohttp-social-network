"""
URLs dispatcher
"""
from handlers.base import Index, Login, SignUp, Logout


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
