from handlers.main.menu import router as index_router
from handlers.main.createStickers import router as createStickers_router
from handlers.main.howWork import router as howWorkRouter

routers = (index_router, createStickers_router, howWorkRouter)
