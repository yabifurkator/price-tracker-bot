from telebot import TeleBot

from database.database import DataBaseConnector
from database.exceptions import FailedToSelectException
from database.mydataclasses import Product
from parser import parse
from mydataclasses import ParseData

from config import \
    PRODUCTS_TABLE_NAME


def parse_endpoint_impl(bot: TeleBot, message):
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

    for line in select_response:
        product = Product(line)
        parse_data: ParseData = parse(product.url)
        try:
            pass
        except RuntimeError:
            pass


