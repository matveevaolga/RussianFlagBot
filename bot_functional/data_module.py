import base64
import aiogram.exceptions
from aiogram.types import input_file, Message


# отправка фотографии и текста пользователю
async def send_data_to_tg(message: Message, info: str, picture: bytes) -> None:
    try:
        # преобразование байтовой picture ??
        picture = base64.b64decode(picture)
        picture = input_file.BufferedInputFile(file=picture, filename=f"flag{message.chat.id}.png")
        await message.answer(info)
        await message.answer_photo(picture)
    except aiogram.exceptions.AiogramError:
        print("failed to send data", "send_data_to_tg")


# sql-запрос для получения фото и информации о флаге
def flags_form(period_name: str, period_time: str) -> str:
    form = f"select periodFlag, flagInfo " \
           f"from historyperiods join flagsinfo" \
           f" on flagsinfo.idFlagPeriod = historyperiods.idPeriod" \
           f" where periodName = '{period_name}' and periodTime = '{period_time}';"
    return form
