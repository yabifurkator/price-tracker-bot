from telebot import TeleBot

from .input_handler import Handler
from .exceptions import InputException
from database.database import DataBaseConnector
from database.database import FailedToDeleteException

from config import \
    PRODUCTS_TABLE_NAME, \
    PRODUCTS_TABLE_URL_COLUMN_NAME


def next_step_handler(message, bot: TeleBot):
    try:
        Handler(message.text)
    except InputException as ex:
        bot.reply_to(message=message, text=ex)
        return
    connection = DataBaseConnector.get_connection()
    sql_request = (
        'DELETE FROM {} '.format(PRODUCTS_TABLE_NAME) +
        'WHERE {url_column_name}={user_input_url}'.format(
            url_column_name=PRODUCTS_TABLE_URL_COLUMN_NAME,
            user_input_url=("'" + message.text + "'")
        )
    )
    try:
        DataBaseConnector.delete(connection=connection, sql_request=sql_request)
    except FailedToDeleteException as ex:
        bot.reply_to(message=message, text=ex)
        return

    text_to_send = (
        'Товар со следующим URL-адресом удалён с отслеживания:\n' +
        message.text
    )
    bot.reply_to(message=message, text=text_to_send)


def delete_endpoint_impl(bot: TeleBot, message):
    text_to_send = (
        'Удаление товара с отслеживания.\n\n'
        'Введите URL-адрес удаляемого товара...'
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
