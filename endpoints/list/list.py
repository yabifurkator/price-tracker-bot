from telebot import TeleBot
import openpyxl
import os

from database.database import DataBaseConnector
from database.mydataclasses import Product
from database.exceptions import FailedToSelectException
from config import \
    PRODUCTS_TABLE_NAME, \
    LIST_PRODUCTS_EXCEL_FILE_NAME


def list_endpoint_impl(bot: TeleBot, message):
    connection = DataBaseConnector.get_connection()
    sql_request = (
        'SELECT {}'.format(Product.select_values_string()) +
        'FROM {}'.format(PRODUCTS_TABLE_NAME)
    )
    try:
        select_response = DataBaseConnector.select(
            connection=connection,
            sql_request=sql_request
        )
    except FailedToSelectException as ex:
        bot.reply_to(message=message, text=ex)
        return

    excel = openpyxl.Workbook()
    sheet = excel.active
    sheet.title = 'Отслеживаемые товары'
    sheet.append(Product.get_excel_data_header())
    for line in select_response:
        sheet.append(line)

    excel.save(LIST_PRODUCTS_EXCEL_FILE_NAME)
    with open(LIST_PRODUCTS_EXCEL_FILE_NAME, 'rb') as file:
        bot.send_document(
            chat_id=message.chat.id,
            document=file,
            reply_to_message_id=message.id,
            caption='Актуальный список товаров на отслеживании.'
        )
    os.remove(LIST_PRODUCTS_EXCEL_FILE_NAME)
