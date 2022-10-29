from telebot import TeleBot

from config import PRICES_ALL_FILE_NAME


def get_endpoint_impl(message, bot: TeleBot):
    try:
        file = open(PRICES_ALL_FILE_NAME, 'rb')
        bot.send_document(
            chat_id=message.chat.id,
            document=file,
            caption="Таблица данных"
        )
    except FileNotFoundError:
        text_to_send = (
            "Файл с таблицей данных не найден.\n"
            "Скорее всего еще не было произведено ни одного сбора цен.\n\n"
            "Чтобы посмотреть текущее состояние цен на данный момент напишите /parse\n"
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=text_to_send
        )
