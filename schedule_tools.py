import os
from datetime import datetime
import openpyxl

from endpoints.parse.parse import get_excel

from config import \
    PRICES_EXCEL_FILE_NAME, \
    ERRORS_EXCEL_FILE_NAME, \
    AUTOSAVE_PATH


def schedule_func():
    try:
        prices_xlsx, errors_xlsx = get_excel()

        try:
            os.mkdir(AUTOSAVE_PATH)
        except FileExistsError:
            pass

        date_format_string = '%m-%d-%Y'

        prices_xlsx_filename = (
            datetime.today().strftime(date_format_string) +
            '_' +
            PRICES_EXCEL_FILE_NAME
        )
        errors_xlsx_filename = (
            datetime.today().strftime(date_format_string) +
            '_' +
            ERRORS_EXCEL_FILE_NAME
        )

        prices_xlsx.save(os.path.join(AUTOSAVE_PATH, prices_xlsx_filename))
        errors_xlsx.save(os.path.join(AUTOSAVE_PATH, errors_xlsx_filename))

        prices_xlsx.close()
        errors_xlsx.close()

    except Exception as ex:
        print(str(ex))
