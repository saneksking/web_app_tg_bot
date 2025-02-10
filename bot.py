import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class TaskStates(StatesGroup):
    title = State()
    description = State()


class TaskEditStates(StatesGroup):
    title = State()
    description = State()


class TelegramBot:
    def __init__(self, token):
        self.bot = Bot(
            token=token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )
        self.dp = Dispatcher()
        self.dp.message(Command("start"))(self.send_welcome)

    async def send_welcome(self, message: types.Message):
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="Get local IP-url",
                callback_data="add_task"
            )
        )
        builder.row(types.InlineKeyboardButton(
            text=f"Get public IP-url",
            callback_data="show_tasks")
        )

        await message.reply(
            f"{os.getenv('WEB_APP_TITLE')}"
            f"\n----------\n"
            f"{os.getenv('WEB_APP_DESCRIPTION')}",
            reply_markup=builder.as_markup()
        )

    async def run(self):
        await self.dp.start_polling(self.bot)


def main():
    api_token = os.getenv("TOKEN")
    bot = TelegramBot(api_token)
    asyncio.run(bot.run())


if __name__ == '__main__':
    main()
