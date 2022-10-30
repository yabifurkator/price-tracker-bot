from telebot import TeleBot

from .input_handler import Handler
from .exceptions import InputException
from database.database import DataBaseConnector
from database.exceptions import DataBaseException
from endpoints.list.list import select_all_products
from endpoints.parse.parser import define_competitor

from config import \
    PRODUCTS_TABLE_NAME, \
    PRODUCTS_TABLE_URL_COLUMN_NAME


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

    try:
        select_response = [url[0] for url in select_all_products(select_values_string='url')]
        print(select_response)
    except DataBaseException as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))
        return

    competitor_to_delete = message.text
    urls_to_delete = []
    for url in select_response:
        competitor = define_competitor(url)
        if competitor is None:
            continue
        if competitor.name == competitor_to_delete:
            urls_to_delete.append(url)

    row_count = 0
    for url in urls_to_delete:
        sql_request = (
                'DELETE FROM {} '.format(PRODUCTS_TABLE_NAME) +
                'WHERE {url_column_name}={url_to_delete}'.format(
                    url_column_name=PRODUCTS_TABLE_URL_COLUMN_NAME,
                    url_to_delete=("'" + url + "'")
                )
        )
        try:
            DataBaseConnector.delete(connection=connection, sql_request=sql_request)
            row_count += 1
        except DataBaseException as ex:
            bot.reply_to(message=message, text=ex)
            return

    if row_count == 0:
        text_to_send = (
            'Товаров с конкурентом "{competitor}" не найдено.'.format(
                competitor=competitor_to_delete
            )
        )
    else:
        text_to_send = (
                'Товары со следущим конкурентом удалены:\n' +
                message.text + '\n'
                'Удалено товаров: {}'.format(row_count)
        )
    bot.reply_to(message=message, text=text_to_send)


def deletecompetitor_endpoint_impl(bot: TeleBot, message):
    text_to_send = (
        'Удаление группы товаров с отслеживания.\n\n'
        'Введите конкурента чьи товары необходимо удалить с отслеживания...'
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
