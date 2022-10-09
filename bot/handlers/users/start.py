from email import message
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.types import Message
from aiogram.types import CallbackQuery, Message
from models import User
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.builtin import Regexp
from bot.commands import get_admin_commands, get_default_commands
from bot.commands import set_admin_commands
from bot.keyboards.inline import *
from loader import dp, _, i18n
from models import User


class Form(StatesGroup):
    name = State()
    social_link = State()
    interests = State()
    expectations = State()
    location = State()

    #dp.bot.send_message(callback_query.message.from_user.id, "text")

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(CommandStart())
async def _start(message: Message, user: User, state: FSMContext):
    if user.is_admin:
        await set_admin_commands(user.id, user.language)

    await state.finish()

    text = (
        "👋 Hola! \n\n"
        "🤖 I'm Web3-native bot from the Web3 Coffee DAO. \n\n"
        "👨‍💻 And I was born to give you an opportunity to go beyond in networking in Web3 world. \n\n"
        "👉 Every week I'll offer you to meet an interesting Web3 guy, randomly selected from other members. \n\n"
        "💡 To take part in the meeting, you need to fill out a form. \n\n"
        "🔗 If I already have some data about you, I'll skip the relevant questions.")

    await message.answer(text, reply_markup=get_start_inline_markup())

@dp.callback_query_handler(Regexp('step_1'))
async def _explanation(callback_query: CallbackQuery):
    text = _("Let's go to basics. That's how everything works")

    photo = open("data/images/explan.jpg", "rb")

    await callback_query.message.answer(text)

    await callback_query.message.answer_photo(photo, reply_markup=get_explanation_inline_markup())

@dp.callback_query_handler(Regexp('step_2'))
async def _nickname(callback_query: CallbackQuery):
    text = _('☕️ What is your .eth nickname? Drop it here or write your name.')

    await Form.name.set()
    await callback_query.message.answer(text)


@dp.message_handler(state=Form.name)
async def _social(message: Message, state: FSMContext):
    text = _("👨‍💻 Send a link to your profile in social media that you actively maintain. \n\n"
        "It will help a person to get to know you in before the first meeting.")

    async with state.proxy() as data:
        data['name'] = message.text

    await Form.next()
    await message.answer(text)


@dp.message_handler(state=Form.social_link)
async def _interests(message: Message, state: FSMContext):
    text = _('👀 What are your work and non-work interests? \n\n'
        '💡 Write words separated by commas that can help to start an interesting conversation')

    async with state.proxy() as data:
        data['social_link'] = message.text

    await Form.next()
    await message.answer(text)


@dp.message_handler(state=Form.interests)
async def _expectations(message: Message, state: FSMContext):
    text = _("⚖️ Some people come to networking to make useful connection and some career-related topics. \n\n"
        "And someone comes to discover something new and expand their horizons. \n\n"
        "💡 Which description suits you best?")

    async with state.proxy() as data:
        data['interests'] = message.text

    await Form.next()
    await message.answer(text, reply_markup=get_expectations_inline_markup())

@dp.callback_query_handler(Regexp('^expectation_(.)'))
async def _format(callback_query: CallbackQuery, regexp: Regexp, state: FSMContext):
    text = _("☕️ Do you prefer online or offline meetings? \n\n"
        "💡 If you choose 'yes', the bot will try to pick up the matching from your city")

    answer = regexp.group(1)

    async with state.proxy() as data:
        if answer == 100: 
            data['expectations'] = "100% work"
        if answer == 70: 
            data['expectations'] = "70% work and 30% fun"
        if answer == 50: 
            data['expectations'] = "50% work and 50% fun"
        if answer == 30: 
            data['expectations'] = "30% work and 70% fun"
        if answer == 00: 
            data['expectations'] = "100% fun"

    await Form.next()
    await callback_query.message.answer(text, reply_markup=get_location_inline_markup())


@dp.callback_query_handler(Regexp('^location_(.)'))
async def _city(callback_query: CallbackQuery, regexp: Regexp, state: FSMContext):
    text = _("☕️ What city are you looking for?")

    answer = regexp.group(1)
    print(f"hey + {answer}")

    async with state.proxy() as data:
        if answer == 1: 
            data['location'] = "online"

    if answer == 2:
        await Form.location.set()
        await callback_query.message.answer(text)
    else:
        await state.finish()
        _final()

@dp.callback_query_handler(state=Form.location)
async def _final(message: Message, regexp: Regexp, state: FSMContext):
    text = _("It's done! 🙌"
        "This is how your profile will look like:")

    await state.finish()
    await message.answer(text)
    _final()

@dp.callback_query_handler(Regexp('profile'))
async def _final(callback_query: CallbackQuery):
    text = _("{username} ({location}) \n"
        "Profile: {social_link} \n\n"
        "What do you do: {career} \n\n"
        "Interests: {interests} \n\n"
        "Expectations: {expectation} \n\n"

        "If you need to change something, just type /help").format()

    await callback_query.message.answer(text, reply_markup=get_explanation_inline_markup())


@dp.message_handler(CommandHelp())
async def _help(message: Message, user: User):
    commands = get_admin_commands(user.language) if user.is_admin else get_default_commands(user.language)

    text = 'Help 🆘' + '\n\n'
    for command in commands:
        text += f'{command.command} - {command.description}\n'

    await message.answer(text)
