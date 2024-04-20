import aioboto3


class S3Storage:
    def __init__(self):
        self.session = aioboto3.Session()
        # TODO: Go config
        self.s3 = self.session.resource(
            service_name='s3',
            endpoint_url='http://localhost:9000/',
            aws_access_key_id='your_access_key',
            aws_secret_access_key='your_secret_key'
        )

    def get_bucket_name(self, pk: int):
        return f'pattern-{pk}'

    async def create_pattern(self, pk: int):
        async with self.s3 as s3:
            await s3.create_bucket(Bucket=self.get_bucket_name(pk))

    async def add_for_pattern(self, pattern_id: int, file):
        async with self.s3 as s3:
            await s3.upload_file(file, self.get_bucket_name(pattern_id), file)


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    async def main():
        s = S3Storage()
        await s.create_pattern(1)
    loop.run_until_complete(main())