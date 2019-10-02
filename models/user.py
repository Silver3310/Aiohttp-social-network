"""
Models for the project
"""
import hashlib

from motor.motor_asyncio import AsyncIOMotorDatabase


class User:
    """
    The User model
    """

    collection = None

    def __init__(self):
        pass

    @staticmethod
    async def get_user(db: AsyncIOMotorDatabase, email: str):
        user = await db.users.find_one({'email': email})
        if user:
            # to avoid the error, because _id is of the ObjectId type
            user['_id'] = str(user['_id'])
            return user
        else:
            return dict(
                error=f'user with email {email} not found'
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
