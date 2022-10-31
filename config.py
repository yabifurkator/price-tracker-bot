import os

TOKEN = os.environ['BK_PRICE_TRACKER_BOT_TOKEN']

TELEGRAM_ID_LIST_FILE_PATH = 'telegram-id-list.txt'

DATABASE_NAME = 'testdb'
DATABASE_USER_NAME = 'leonidpsql'
DATABASE_USER_PASSWORD = 'password'
DATABASE_HOST = 'localhost'
DATABASE_PORT = '5432'

PRODUCTS_TABLE_NAME = 'products'
PRODUCTS_TABLE_BARCODE_COLUMN_NAME = 'barcode'
PRODUCTS_TABLE_SKU_COLUMN_NAME = 'sku'
PRODUCTS_TABLE_URL_COLUMN_NAME = 'url'

USERS_TABLE_NAME = 'users'

LIST_PRODUCTS_EXCEL_FILE_NAME = 'products.xlsx'
PRICES_EXCEL_FILE_NAME = 'prices.xlsx'
ERRORS_EXCEL_FILE_NAME = 'errors.xlsx'

PRICES_ALL_FILE_NAME = 'prices_all.xlsx'

NONE_PRICE_PLACEHOLDER = '-'

# datetime.today().strftime(DATE_FORMAT_STRING)
DATE_FORMAT_STRING = '%m/%d/%Y'
AUTOSAVE_FOLDER_NAME = 'autosave'
AUTOSAVE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    AUTOSAVE_FOLDER_NAME
)
