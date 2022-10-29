from telebot import TeleBot

from .input_handler import Handler
from .exceptions import InputException
from database.database import DataBaseConnector
from database.mydataclasses import Product
from database.exceptions import FailedToInsertException

from config import \
    PRODUCTS_TABLE_NAME, \
    PRODUCTS_TABLE_BARCODE_COLUMN_NAME, \
    PRODUCTS_TABLE_SKU_COLUMN_NAME, \
    PRODUCTS_TABLE_URL_COLUMN_NAME


def next_step_handler(message, bot: TeleBot):
    try:
        handler = Handler(text=message.text)
        data_class = handler.products_table_data_class
    except InputException as ex:
        bot.reply_to(message=message, text=ex)
        return

    try:
        connection = DataBaseConnector.get_connection()
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))
        return

    sql_request = (
        'INSERT INTO {} '.format(PRODUCTS_TABLE_NAME) +
        data_class.insert_values_string() +
        ' VALUES {}'.format(data_class.insert_values_to_string())
    )
    try:
        DataBaseConnector.insert(connection=connection, sql_request=sql_request)
    except FailedToInsertException as ex:
        bot.reply_to(message=message, text=ex)
        return

    text_to_send = (
        'Товар добавлен на отслеживание.\n\n'
        'Штрих-Код: {}\n'.format(data_class.barcode) +
        'SKU: {}\n'.format(data_class.sku) +
        'URL-адрес: {}\n'.format(data_class.url)
    )
    bot.reply_to(message=message, text=text_to_send)


def add_endpoint_impl(bot: TeleBot, message):
    text_to_send = (
        'Добавление товара на отслеживание.\n\n'
        'Введите данные о товаре в следующем виде:\n'
        '1-я строка: Штрих-Код\n'
        '2-я строка: SKU\n'
        '3-я строка: URL-адрес товара\n'
    )
    next_step_handler_message = bot.reply_to(
        message=message,
        text=text_to_send
    )
    bot.register_next_step_handler(
        next_step_handler_message,
        next_step_handler,
        bot
    )
