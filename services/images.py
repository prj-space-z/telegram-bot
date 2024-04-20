from aiogram import Bot
import io
from PIL import Image


async def downloading_image(bot: Bot, image_id: str) -> io.BytesIO:
    file = await bot.get_file(image_id)
    image_in_memory = io.BytesIO()
    await bot.download_file(file.file_path, destination=image_in_memory)
    return image_in_memory


async def resizing_image(buffer) -> io.BytesIO:
    image_io = io.BytesIO()

    img = Image.open(buffer)
    img = img.convert('RGB')
    img = img.resize((512, 512))
    img.save(image_io, 'WEBP')
    return image_io
