from telebot import TeleBot
import openpyxl
import io

from database.database import DataBaseConnector
from database.exceptions import DataBaseException
from config import PRODUCTS_TABLE_NAME
from database.mydataclasses import Product


def next_step_handler(message, bot: TeleBot):
    if message.document is None:
        text_to_send = (
            'Ошибка. В отправленном сообщении нет документа.'
        )
        bot.reply_to(
            message=message,
            text=text_to_send
        )
        return
    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    if not message.document.mime_type == mime_type:
        text_to_send = (
            'Отправленный Вами документ не является xlsx таблицей.'
        )
        bot.reply_to(
            message=message,
            text=text_to_send
        )
        return

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    xlsx = openpyxl.load_workbook(io.BytesIO(downloaded_file))
    iterator = iter(xlsx.active)
    try:
        next(iterator)
    except StopIteration:
        text_to_send = (
            'xlsx файл должен содержать хотя бы одну строку.'
        )
        bot.reply_to(
            message=message,
            text=text_to_send
        )
        return

    try:
        connection = DataBaseConnector.get_connection()
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))
        return

    try:
        sql_request = 'DELETE FROM {};'.format(PRODUCTS_TABLE_NAME)
        DataBaseConnector.delete(connection=connection, sql_request=sql_request)
    except DataBaseException as ex:
        pass

    line_errors = []
    success_count = 0
    for line in iterator:
        line_list = [str(cell.value) for cell in line]
        if len(line_list) != 3:
            line_list.append('Количество столбцов в строке не равно трём.')
            line_errors.append(line_list)
            continue
        product = Product(
            barcode=line_list[0],
            sku=line_list[1],
            url=line_list[2]
        )

        sql_request = (
            'INSERT INTO {} '.format(PRODUCTS_TABLE_NAME) +
            product.insert_values_string() +
            ' VALUES {}'.format(product.insert_values_to_string())
        )
        try:
            DataBaseConnector.insert(connection=connection, sql_request=sql_request)
            success_count += 1
        except DataBaseException as ex:
            line_list.append(ex.reason)
            line_errors.append(line_list)
            continue
        except Exception as ex:
            line_list.append(str(ex))
            line_errors.append(line_list)
            continue

    errors_xlsx = openpyxl.Workbook()
    sheet = errors_xlsx.active
    excel_data_header = Product.get_excel_data_header()
    excel_data_header.append('Причина')
    sheet.append(excel_data_header)
    for line in line_errors:
        sheet.append(line)

    response_bytes_io = io.BytesIO()
    errors_xlsx.save(response_bytes_io)

    bot_message = bot.reply_to(
        message=message,
        text='Успешно добавлено товаров: {}'.format(success_count)
    )
    bot.send_document(
        chat_id=message.chat.id,
        reply_to_message_id=bot_message.id,
        document=response_bytes_io.getbuffer(),
        caption='Отчёт об ошибках добавления',
        visible_file_name='response.xlsx'
    )


def loadxlsx_endpoint_impl(bot: TeleBot, message):
    text_to_send = (
        'Загрузка списка товаров на отслеживание.\n'
        'Отправьте xlsx файл с данными о товарах.'
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
