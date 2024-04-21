import time
from decouple import config
import motor.motor_asyncio
import time
from settings import Settings
from transliterate import translit, get_available_language_codes
from redis.asyncio import Redis


settings = Settings()
redis = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
)


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
            'is_share': share,
            'created_at': time.time(),
        }
        await self.patterns_collection.insert_one(data)
        return data

    async def get_patterns(self, js: dict) -> list:
        return [data async for data in self.patterns_collection.find(js)]

    async def get_patterns_count(self):
        return await self.patterns_collection.count_documents({})

    async def create_user(self, user_id: int):
        data = {
            'user_id': user_id,
            'created_at': time.time(),
        }

        await self.user_collection.insert_one(data)

    async def get_user(self, user_id: int):
        return await self.user_collection.find_one({'user_id': user_id})

    async def get_pattern(self, pattern_id: int) -> dict:
        return await self.patterns_collection.find_one({'id': pattern_id})

    async def edit_pattern(self, pattern_id: int, data: dict):
        await self.patterns_collection.update_one({'id': pattern_id}, {'$set': data})

    async def delete_pattern(self, pattern_id: int):
        await self.patterns_collection.delete_one({'id': pattern_id})

    async def get_user_count(self, time_h: int = None):
        if time_h is None:
            return await self.user_collection.count_documents({})
        else:
            start_time = time.time() - time_h * 60 * 60
            query = {'created_at': {'$gte': start_time, '$lte': time.time()}}
            return await self.user_collection.count_documents(query)

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

    async def edit_settings(self, js: dict):
        return await self.settings_collection.update_one({}, {'$set': js})


db = DataBase(Settings().mongodb_url.get_secret_value())
