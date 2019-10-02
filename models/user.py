"""
Models for the project
"""


class User:
    """
    The User model
    """

    collection = None

    def __init__(self):
        pass

    @staticmethod
    async def get_user(db, uid):
        return db.users.find_one(uid)
