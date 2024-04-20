# import boto3
# session = boto3.session.Session()
# s3 = session.client(
#     service_name='s3',
#     endpoint_url='http://localhost:9000/',
#     aws_access_key_id='your_access_key',
#     aws_secret_access_key='your_secret_key',
# )
#
# print(s3.list_buckets())
#
# s3.create_bucket(Bucket='bucket-name')

import aioboto3
async def main():
    session = aioboto3.Session()
    s3 = await session.resource(service_name='s3', endpoint_url='http://localhost:9000/', aws_access_key_id='your_access_key', aws_secret_access_key='your_secret_key',)
    print(s3.buckets.all())

import asyncio
asyncio.run(main())