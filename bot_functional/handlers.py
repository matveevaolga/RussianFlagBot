import aiogram.exceptions
import pymysql
from bd_functional.bd_connection import DBConnection
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot_functional.bot_lexicon import lexicon
from aiogram import Router
from bot_functional.keyboards import Keyboards
from bot_functional.data_module import send_data_to_tg, flags_form

router: Router = Router()


# обработка команды /start
@router.message(Command(commands="start"))
async def process_start_command(message: Message):
    try:
        await message.answer(text=lexicon["/start"])
    except aiogram.exceptions.AiogramError:
        print("failed to process command", "process_start_command")


# обработка команды /flags
@router.message(Command(commands="flags"))
async def process_flags_command(message: Message):
    try:
        keyboards = Keyboards()
        flags_keyboard = keyboards.keyboard
        # отправка сообщения и сформированной клавиатуры
        await message.answer(text=lexicon["/flags"], reply_markup=flags_keyboard)
    except aiogram.exceptions.AiogramError:
        print("failed to process command", "process_flags_command")


# обработка команды /additional
@router.message(Command(commands="additional"))
async def process_additional_command(message: Message):
    try:
        keyboards = Keyboards(True)
        additional_keyboard = keyboards.keyboard
        # отправка сообщения и сформированной клавиатуры
        await message.answer(text=lexicon["/additional"], reply_markup=additional_keyboard)
    except aiogram.exceptions.AiogramError:
        print("failed to process command", "process_additional_command")


@router.callback_query(lambda callback: " add" in callback.data)
async def additional_info(callback: CallbackQuery):
    message = callback.message
    request = callback.data.replace(" add", "")
    connection = DBConnection()
    if not connection:
        return
    connection.open_connect()
    cursor = connection.get_cursor()
    try:
        cursor.execute(f"select infoText, infoPicture from additionalinfo where infoName = '{request}';")
        info, image = cursor.fetchone()
    except pymysql.Error:
        print("failed to commit sql-query", "additional_info")
        return
    await send_data_to_tg(message, info, image)
    connection.close_connect()
    await callback.answer()


@router.callback_query()
async def flags_info(callback: CallbackQuery):
    message = callback.message
    connection = DBConnection()
    if not connection.connection:
        return
    connection.open_connect()
    cursor = connection.get_cursor()
    period_name, period_time = callback.data.split('\n')
    try:
        cursor.execute(flags_form(period_name, period_time))
        info, image = "", ""
        for picture, info_piece in cursor.fetchall():
            info += info_piece + '\n'
            image = picture
    except pymysql.Error:
        print("failed to commit sql-query", "flags_info")
        return
    info = info.strip()
    await send_data_to_tg(message, info, image)
    connection.close_connect()
    await callback.answer()
