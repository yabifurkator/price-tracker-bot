from telebot import TeleBot
import os
from datetime import datetime
import openpyxl

from database.database import DataBaseConnector
from database.exceptions import FailedToSelectException
from database.mydataclasses import Product
from .parser import parse
from .mydataclasses import \
    ParseData, \
    PriceLine, \
    ErrorLine

from .exceptions import ParseException

from config import \
    PRODUCTS_TABLE_NAME, \
    PRICES_EXCEL_FILE_NAME, \
    ERRORS_EXCEL_FILE_NAME


def get_excel(bot: TeleBot=None, message=None):
    connection = DataBaseConnector.get_connection()
    sql_request = (
        'SELECT {}'.format(Product.select_values_string()) +
        'FROM {}'.format(PRODUCTS_TABLE_NAME)
    )
    select_response = DataBaseConnector.select(
            connection=connection,
            sql_request=sql_request
    )

    prices_lines = []
    errors_lines = []

    def get_current_date():
        return datetime.today().strftime('%m/%d/%Y')

    if bot:
        edit_message_template = 'Прогресс: {current}\\' + str(len(select_response))
        text_to_send = edit_message_template.format(current=0)
        edit_message = bot.reply_to(message=message, text=text_to_send)

    line_counter = 0
    for line in select_response:
        if bot:
            line_counter += 1
            text_to_send = edit_message_template.format(current=line_counter)
            bot.edit_message_text(
                chat_id=edit_message.chat.id,
                message_id=edit_message.message_id,
                text=text_to_send
            )

        product = Product.init_by_line(line)
        try:
            parse_data: ParseData = parse(product.url)
            price_line = PriceLine(
                barcode=product.barcode,
                sku=product.sku,
                competitor_name=parse_data.competitor_name,
                date=get_current_date(),
                default_price=parse_data.price_to_string(parse_data.default_price),
                promo_price=parse_data.price_to_string(parse_data.promo_price),
                url=product.url
            )
            prices_lines.append(price_line)
        except ParseException as ex:
            error_line = ErrorLine(
                barcode=product.barcode,
                sku=product.sku,
                date=get_current_date(),
                reason=ex.reason,
                url=ex.url
            )
            errors_lines.append(error_line)
        except Exception as ex:
            error_line = ErrorLine(
                barcode=product.barcode,
                sku=product.sku,
                date=get_current_date(),
                reason=str(ex),
                url=product.url
            )
            errors_lines.append(error_line)

    prices_xlsx = openpyxl.Workbook()
    prices_sheet = prices_xlsx.active
    prices_sheet.append(PriceLine.get_excel_data_header())
    for line in prices_lines:
        prices_sheet.append(line.to_excel_line())

    errors_xlsx = openpyxl.Workbook()
    errors_sheet = errors_xlsx.active
    errors_sheet.append(ErrorLine.get_excel_data_header())
    for line in errors_lines:
        errors_sheet.append(line.to_excel_line())

    return prices_xlsx, errors_xlsx


def parse_endpoint_impl(bot: TeleBot, message):
    bot_message = bot.send_message(message.chat.id, 'Начало парсинга, ждите...')

    try:
        prices_xlsx, errors_xlsx = get_excel(bot=bot, message=bot_message)
        prices_xlsx.save(PRICES_EXCEL_FILE_NAME)

        errors_xlsx.save(ERRORS_EXCEL_FILE_NAME)

        with open(PRICES_EXCEL_FILE_NAME, 'rb') as prices_xlsx_file, \
             open(ERRORS_EXCEL_FILE_NAME, 'rb') as errors_xlsx_file:
            bot_message = bot.send_document(
                chat_id=message.chat.id,
                document=prices_xlsx_file,
                caption='Актуальная таблица с ценами',
                reply_to_message_id=message.id
            )
            bot.send_document(
                chat_id=message.chat.id,
                document=errors_xlsx_file,
                caption='Возникшие в ходе получения актуальных цен ошибки',
                reply_to_message_id=bot_message.id
            )

        os.remove(PRICES_EXCEL_FILE_NAME)
        os.remove(ERRORS_EXCEL_FILE_NAME)
    except Exception as ex:
        bot.reply_to(message=message, text=str(ex))
        return
