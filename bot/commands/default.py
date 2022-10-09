from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat, BotCommand

from loader import _, bot, i18n
from typing import List


def get_default_commands(lang: str = 'en') -> List[BotCommand]:
    commands = [
        #BotCommand('/start', _('start bot', locale=lang)),
    ]

    return commands


async def set_default_commands():
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())

    # for lang in i18n.available_locales:
    #     await bot.set_my_commands(get_default_commands(lang), scope=BotCommandScopeDefault(), language_code=lang)


async def set_user_commands(user_id: int, commands_lang: str):
    await bot.set_my_commands(get_default_commands(commands_lang), scope=BotCommandScopeChat(user_id))
