import logging
from factory import create_dispatcher, create_bot
from typing import cast
from settings import Settings

logging.basicConfig(level=logging.INFO)


def run_bot():
    dp = create_dispatcher()
    bot = create_bot(settings=cast(Settings, dp["settings"]))
    return dp.run_polling(bot)


if __name__ == '__main__':
    run_bot()
