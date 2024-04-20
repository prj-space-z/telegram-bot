from aiogram import Router
from filters import PRIVATE_ONLY
from . import menu, howWork, createStickers, createPattern

router = Router(name=__name__)
router.message.filter(PRIVATE_ONLY)
router.include_routers(menu.router, howWork.router, createStickers.router, createPattern.router)
