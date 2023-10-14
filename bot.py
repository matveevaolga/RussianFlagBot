import asyncio
import aiogram.exceptions
from bot_functional.config import bot_config
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot_functional.handlers import router


# создание меню
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="О боте"),
        BotCommand(command='/flags', description='Развитие русского флага'),
        BotCommand(command='/additional', description='Интересные факты')]
    await bot.set_my_commands(main_menu_commands)


async def main():
    try:
        # инициализация бота и диспетчера
        bot_token = bot_config["token"]
        bot = Bot(token=bot_token)
        dispatcher = Dispatcher()
        # регистрация роутера
        dispatcher.include_router(router)
        # меню будет создаваться при запуске бота
        dispatcher.startup.register(set_main_menu)
        # запуск бота
        await dispatcher.start_polling(bot)
    except aiogram.exceptions.AiogramError:
        print("failed to run bot", "main")

if __name__ == '__main__':
    asyncio.run(main())
