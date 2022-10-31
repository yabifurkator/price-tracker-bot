from telebot import TeleBot

import io
import glob
import openpyxl
from endpoints.parse.mydataclasses import \
    PriceLine, \
    ErrorLine
from config import \
    AUTOSAVE_PATH, \
    PRICES_EXCEL_FILE_NAME, \
    ERRORS_EXCEL_FILE_NAME


def merge_xlsxlist_to_xlsx(xlsx_list, first_line):
    xlsx_merged = openpyxl.Workbook()
    xlsx_merged_sheet = xlsx_merged.active

    xlsx_merged_sheet.append(first_line)
    for xlsx in xlsx_list:
        iterator = iter(xlsx.active)
        next(iterator)
        for line in iterator:
            row = [cell.value for cell in line]
            xlsx_merged_sheet.append(row)

    return xlsx_merged


def merge_xlsx(filename_pattern, first_line):
    filelist = glob.glob(filename_pattern)
    xlsx_list = []
    for file in filelist:
        xlsx = openpyxl.load_workbook(filename=file)
        xlsx_list.append(xlsx)
    xlsx_merged = merge_xlsxlist_to_xlsx(xlsx_list, first_line=first_line)
    return xlsx_merged


def send_xlsx(bot: TeleBot, message, xlsx: openpyxl.Workbook, visible_file_name, caption):
    xlsx_bytes = io.BytesIO()
    xlsx.save(xlsx_bytes)
    bot_message = bot.send_document(
        chat_id=message.chat.id,
        document=xlsx_bytes.getbuffer(),
        visible_file_name=visible_file_name,
        reply_to_message_id=message.id,
        caption=caption
    )
    return bot_message


def get_endpoint_impl(bot: TeleBot, message):
    prices_xlsx_merged = merge_xlsx(
        filename_pattern=AUTOSAVE_PATH + '/*{}'.format(PRICES_EXCEL_FILE_NAME),
        first_line=PriceLine.get_excel_data_header()
    )
    errors_xlsx_merged = merge_xlsx(
        filename_pattern=AUTOSAVE_PATH + '/*{}'.format(ERRORS_EXCEL_FILE_NAME),
        first_line=ErrorLine.get_excel_data_header()
    )

    bot_message = send_xlsx(
        bot=bot,
        message=message,
        xlsx=prices_xlsx_merged,
        visible_file_name='prices_merged.xlsx',
        caption='Результирующая таблица цен'
    )
    send_xlsx(
        bot=bot,
        message=bot_message,
        xlsx=errors_xlsx_merged,
        visible_file_name='errors_merged.xlsx',
        caption='Результирующая таблица ошибок'
    )
