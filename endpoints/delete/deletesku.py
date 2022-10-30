from telebot import TeleBot

from .input_handler import Handler
from .exceptions import InputException
from database.database import DataBaseConnector
from database.database import FailedToDeleteException

from config import \
    PRODUCTS_TABLE_NAME, \
    PRODUCTS_TABLE_SKU_COLUMN_NAME


def next_step_handler(message, bot: TeleBot):
    try:
        Handler(message.text)
    except InputException as ex:
        bot.reply_to(message=message, text=ex)
        return

    try:
        connection = DataBaseConnector.get_connection()
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))
        return

    sql_request = (
            'DELETE FROM {} '.format(PRODUCTS_TABLE_NAME) +
            'WHERE {sku_column_name}={user_input_sku}'.format(
                sku_column_name=PRODUCTS_TABLE_SKU_COLUMN_NAME,
                user_input_sku=("'" + message.text + "'")
            )
    )
    try:
        row_count = DataBaseConnector.delete(connection=connection, sql_request=sql_request)
    except FailedToDeleteException as ex:
        bot.reply_to(message=message, text=ex)
        return

    text_to_send = (
            'Товары со следующим SKU удалёны с отслеживания:\n' +
            message.text + '\n'
            'Удалено товаров: {}'.format(row_count)
    )
    bot.reply_to(message=message, text=text_to_send)


def deletesku_endpoint_impl(bot: TeleBot, message):
    text_to_send = (
        'Удаление группы товаров с отслеживания.\n\n'
        'Введите SKU удаляемых товаров...'
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
