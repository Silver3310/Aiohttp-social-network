"""
Model User for the project
"""
import hashlib

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class User:
    """
    The User model
    """

    def __init__(self):
        pass

    @staticmethod
    async def get_user(db: AsyncIOMotorDatabase, email: str):
        user = await db.users.find_one({'email': email})
        if user:
            # to avoid the error, because _id is of the ObjectId type
            user['_id'] = str(user['_id'])
            if 'friends' in user:
                user['friends'] = [str(uid) for uid in user['friends']]
            return user
        else:
            return dict(
                error=f'user with email {email} not found'
            )

    @staticmethod
    async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str):
        user = await db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            # to avoid the error, because _id is of the ObjectId type
            user['_id'] = str(user['_id'])
            if 'friends' in user:
                user['friends'] = [str(uid) for uid in user['friends']]
            return user
        else:
            return dict(
                error=f'user with id {user_id} not found'
            )

    @staticmethod
    async def create_new_user(db: AsyncIOMotorDatabase, data):
        """
        Function for creating a new user

        :param db: AsyncIOMotorDatabase
        :param data: data from the form
        :return: result from MongoDB (dict)
        """

        email = data['email']
        user = await db.users.find_one({'email': email})
        if user:
            return dict(
                error=f'user with email {email} exists'
            )

        if data['first_name'] and data['last_name'] and data['password']:
            # data is not dict initially
            data = dict(data)
            data['password'] = hashlib.sha256(
                data['password'].encode('utf-8')
            ).hexdigest()

            # write to the Users' collection
            result = await db.users.insert_one(data)
            return result
        else:
            return dict(
                error='Missing user data parameters'
            )

    @staticmethod
    async def save_avatar_url(
            db: AsyncIOMotorDatabase,
            user_id: str,
            url: str
    ):
        """Save profile picture"""

        if url and user_id:
            db.users.update_one(
                {'_id': ObjectId(user_id)},
                {'$set': {'avatar_url': url}}
            )

    @staticmethod
    async def get_user_friends_suggestions(
            db: AsyncIOMotorDatabase,
            user_id: str,
            limit=20
    ):
        """Show all users except for the current one"""

        query = {'_id': {'$ne': ObjectId(user_id)}}
        users = await db.users.find(query).to_list(limit)
        return users

    @staticmethod
    async def add_friend(
            db: AsyncIOMotorDatabase,
            user_id: str,
            friend_id: str
    ):
        """Add a friend"""

        await db.users.update_one(
            {'_id': ObjectId(user_id)},
            # $addToSet appends an element to a list
            {'$addToSet': {'friends': ObjectId(friend_id)}}
        )

    @staticmethod
    async def get_user_friends(
            db: AsyncIOMotorDatabase,
            user_id: str,
            limit=20
    ):
        """Show a list of friends"""

        user = await db.users.find_one({'_id': ObjectId(user_id)})
        user_friends = await db.users.find(
            {'_id': {'$in': user['friends']}}
        ).to_list(limit)
        return user_friends
