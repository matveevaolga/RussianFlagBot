import aiogram.exceptions
import pymysql
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bd_functional.bd_connection import DBConnection


class Keyboards:
    def __init__(self, is_additional=False):
        try:
            self.connection = DBConnection()
            self.connection.open_connect()
            self.cursor = self.connection.get_cursor()
            if is_additional:
                self.keyboard = self.form_additional_keyboard()
            else:
                self.keyboard = self.form_flags_keyboard()
            self.connection.close_connect()
        except pymysql.Error:
            self.connection = None
            print("failed to connect to database", "Keyboards class")

    # создание клавиатуры с интересными фактами
    def form_additional_keyboard(self) -> InlineKeyboardMarkup | None:
        # создание массива
        keyboard: list[InlineKeyboardButton] = []
        try:
            self.cursor.execute("select infoName from additionalinfo")
            facts: list = [x[0] for x in self.cursor.fetchall()]
        except pymysql.Error:
            print("failed to commit sql-query", "form_additional_keyboard")
            # как тут лучше сделать? все же вернуть None?
            return
        try:
            # наполнение массива кнопками
            for category in facts:
                new_button: InlineKeyboardButton = InlineKeyboardButton(
                    text=category,
                    callback_data=category + " add"
                )
                keyboard.append(new_button)
            # формирование клавиатуры
            keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
            keyboard_builder.row(*keyboard, width=1)
            return keyboard_builder.as_markup(resize_keyboard=True)
        except aiogram.exceptions.AiogramError:
            print("failed to form keyboard", "form_additional_keyboard")

    # создание клавиатуры с информацией о флагах
    def form_flags_keyboard(self):
        # создание массива
        keyboard: list[InlineKeyboardButton] = []
        try:
            self.cursor.execute("select periodName, periodTime from historyperiods")
            flags: list = [x for x in self.cursor.fetchall()]
        except pymysql.Error:
            print("failed to commit sql-query", "form_flags_keyboard")
            # как тут лучше сделать? все же вернуть None?
            return
        try:
            # наполнение массива кнопками
            for period_name, period_time in flags:
                current_flag = f"{period_name}\n{period_time}"
                new_button: InlineKeyboardButton = InlineKeyboardButton(
                    text=current_flag,
                    callback_data=current_flag
                )
                keyboard.append(new_button)
            # формирование клавиатуры
            keyboard_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
            keyboard_builder.row(*keyboard, width=1)
            return keyboard_builder.as_markup(resize_keyboard=True)
        except aiogram.exceptions.AiogramError:
            print("failed to form keyboard", "form_flags_keyboard")

