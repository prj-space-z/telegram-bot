import io
from settings import Settings
from celery import Celery
from .s3_storage import s3
from .face_swap_api import face_swap
from aiogram import Bot
import asyncio


app = Celery(__name__, broker=Settings().celery_broker.get_secret_value(), backend=Settings().celery_broker.get_secret_value(), include=[__name__])

app.conf.event_serializer = 'pickle'
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']


@app.task(name="face_swap")
def create_stickers_task(photos_pack: [io.BytesIO], image_in_memory: io.BytesIO):
    photos = []

    for photo in photos_pack:
        photos.append(face_swap.face_swap(photo, image_in_memory))
    return [photo.read() for photo in photos]
