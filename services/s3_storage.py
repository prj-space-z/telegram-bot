from miniopy_async import Minio
from miniopy_async.commonconfig import Tags
import random
import string
import io
import aiohttp


class S3Storage:
    buckets = ['patterns']

    def __init__(self):
        #TODO: Go conf
        self.client = Minio(
            "localhost:9000",
            access_key="your_access_key",
            secret_key="your_secret_key",
            secure=False
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


s3 = S3Storage()

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()

    async def main():
        s = S3Storage()
        await s.get_patterns_photos(1)

    loop.run_until_complete(main())