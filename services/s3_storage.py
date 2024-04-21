from miniopy_async import Minio
from miniopy_async.commonconfig import Tags
import random
import string
import io
import aiohttp
from settings import Settings


class S3Storage:
    buckets = ['patterns']

    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool):
        self.client = Minio(
            endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    async def init(self):
        for bucket in self.buckets:
            found = await self.client.bucket_exists(bucket)
            if not found:
                await self.client.make_bucket(bucket)

    async def add_patterns_photo(self, photos: list[io.BytesIO], pattern_id: int):
        tags = Tags(for_object=True)
        tags["pattern"] = str(pattern_id)

        for photo in photos:
            await self.client.put_object(bucket_name='patterns',
                                         object_name=''.join(random.choices(string.hexdigits, k=10)),
                                         length=int(len(photo.read())),
                                         data=io.BytesIO(photo.getbuffer()),
                                         tags=tags)

    async def get_patterns_photos(self, pattern_id: int) -> list[io.BytesIO]:
        photos = []

        for photo in await self.client.list_objects('patterns'):
            tags = await self.client.get_object_tags('patterns', photo.object_name)
            if tags.get('pattern') == str(pattern_id):
                async with aiohttp.ClientSession() as session:
                    file = await self.client.get_object('patterns', photo.object_name, session)
                    photos.append(io.BytesIO(await file.read()))

        return photos


settings = Settings()
s3 = S3Storage(
    settings.minio_endpoint,
    settings.minio_access_key.get_secret_value(),
    settings.minio_secret_key.get_secret_value(),
    settings.minio_secure
)
