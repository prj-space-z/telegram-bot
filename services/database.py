import time
from decouple import config
import motor.motor_asyncio
import time
from settings import Settings
from transliterate import translit, get_available_language_codes


class DataBase:
    """
    Designed to work with the database
    """

    def __init__(self, url_connect: str = None):
        self.url_connect = url_connect
        self.cluster = motor.motor_asyncio.AsyncIOMotorClient(url_connect)
        self.user_collection = self.cluster.MemeSwap.users
        self.settings_collection = self.cluster.MemeSwap.settings
        self.patterns_collection = self.cluster.MemeSwap.patterns

    async def create_patterns(self, name: str, user_id: int, share: bool = False) -> dict:
        data = {
            'id': await self.patterns_collection.count_documents({}) + 1,
            'name': name,
            'translit': translit(name, 'ru', reversed=True),
            'user_id': user_id,
            'is_share': share
        }
        await self.patterns_collection.insert_one(data)
        return data

    async def create_user(self, user_id: int):
        data = {
            'user_id': user_id,
            'created_at': time.time(),
        }

        await self.user_collection.insert_one(data)

    async def get_user(self, user_id: int):
        return await self.user_collection.find_one({'user_id': user_id})

    async def settings_init(self):
        if await self.settings_collection.count_documents({}) == 0:
            data = {
                'technical_work': False,
                'social': {
                    'vk': {
                        'active': False,
                        'token': None,
                        'url': None,
                    },
                    'telegram': {
                        'active': False,
                        'url': None,
                        'channel_id': None,
                    }
                }
            }

            await self.settings_collection.insert_one(data)

    async def get_settings(self):
        return await self.settings_collection.find_one({})


db = DataBase(Settings().mongodb_url.get_secret_value())
