"""
--------------------------------------------------------
Licensed under the terms of the BSD 3-Clause License
(see LICENSE for details).
Copyright © 2025, A.A. Suvorov
All rights reserved.
--------------------------------------------------------
"""
import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from utils.get_ip import get_local_ip, get_public_ip


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


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
        self.dp.callback_query()(self.handle_callback_query)

    async def handle_callback_query(self, callback_query: types.CallbackQuery):
        await callback_query.answer()

        if callback_query.data == "show_local_ip":
            await self.get_local_url(callback_query.message)
        elif callback_query.data == "show_public_ip":
            await self.get_public_url(callback_query.message)
        elif callback_query.data == "back":
            await self.send_welcome(callback_query.message)

    @staticmethod
    async def send_welcome(message: types.Message):
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="Get local IP-url",
                callback_data="show_local_ip"
            )
        )
        builder.row(types.InlineKeyboardButton(
            text="Get public IP-url",
            callback_data="show_public_ip")
        )

        await message.reply(
            f"{os.getenv('WEB_APP_TITLE')}"
            f"\n----------\n"
            f"{os.getenv('WEB_APP_DESCRIPTION')}",
            reply_markup=builder.as_markup()
        )

    @staticmethod
    async def get_local_url(message: types.Message):
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="<- Back",
                callback_data="back"
            )
        )
        await message.answer(
            f"URL: {get_local_ip()}:{os.getenv('PORT')}",
            reply_markup=builder.as_markup())

    @staticmethod
    async def get_public_url(message: types.Message):
        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text="<- Back",
                callback_data="back"
            )
        )
        await message.answer(
            f"URL: {get_public_ip()}:{os.getenv('PORT')}",
            reply_markup=builder.as_markup())

    async def run(self):
        await self.dp.start_polling(self.bot)


def main():
    api_token = os.getenv("TOKEN")
    bot = TelegramBot(api_token)
    asyncio.run(bot.run())


if __name__ == '__main__':
    main()
