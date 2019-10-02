"""
URLs dispatcher
"""
from handlers.base import index, login, signup


def setup_routers(app):
    app.router.add_get('/', index)
    app.router.add_get('/login', login)
    app.router.add_get('/signup', signup)
