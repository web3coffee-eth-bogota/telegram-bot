from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery

from services.users import get_or_create_user
from typing import List

class UsersMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: Message, data: List[str]):
        if 'channel_post' in message or message.chat.type != 'private':
            raise CancelHandler()

        await message.answer_chat_action('typing')

        user = message.from_user

        data['user'] = get_or_create_user(user.id, user.full_name, user.username, user.language_code)

    @staticmethod
    async def on_process_callback_query(callback_query: CallbackQuery, data: List[str]):
        user = callback_query.from_user

        data['user'] = get_or_create_user(user.id, user.full_name, user.username, user.language_code)

    @staticmethod
    async def on_process_inline_query(inline_query: InlineQuery, data: List[str]):
        user = inline_query.from_user

        data['user'] = get_or_create_user(user.id, user.full_name, user.username, user.language_code)
