import openpyxl

from endpoints.parse.parse import get_excel
from endpoints.parse.mydataclasses import PriceLine
from config import PRICES_ALL_FILE_NAME


def schedule_func():
    try:
        prices_all_excel = openpyxl.load_workbook(PRICES_ALL_FILE_NAME)
    except FileNotFoundError:
        prices_all_excel = openpyxl.Workbook()
        prices_all_excel.active.append(PriceLine.get_excel_data_header())

    prices_all_worksheet = prices_all_excel.active
    prices_all_worksheet.title = 'Таблица'

    excel, error_excel = get_excel()

    excel_worksheet = excel.active

    iterator = iter(excel_worksheet)
    next(iterator)
    for line in iterator:
        row = [cell.value for cell in line]
        prices_all_worksheet.append(row)

    prices_all_excel.save(PRICES_ALL_FILE_NAME)
