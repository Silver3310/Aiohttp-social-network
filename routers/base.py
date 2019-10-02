"""
URLs dispatcher
"""
from handlers.base import Index, Login, SignUp


def setup_routers(app):
    app.router.add_get('/', Index.get)
    app.router.add_get('/login', Login.get)
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', SignUp.get)
