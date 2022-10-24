from dataclasses import dataclass

from config import \
    PRODUCTS_TABLE_NAME, \
    PRODUCTS_TABLE_BARCODE_COLUMN_NAME, \
    PRODUCTS_TABLE_SKU_COLUMN_NAME, \
    PRODUCTS_TABLE_URL_COLUMN_NAME, \
    LIST_PRODUCTS_EXCEL_FILE_NAME


@dataclass
class Product:
    barcode: str
    sku: str
    url: str

    @staticmethod
    def init_by_line(line):
        product = Product(
            barcode=line[0],
            sku=line[1],
            url=line[2]
        )
        return product

    @staticmethod
    def select_values_string():
        return '{barcode_column_name}, {sku_column_name}, {url_column_name} '.format(
            barcode_column_name=PRODUCTS_TABLE_BARCODE_COLUMN_NAME,
            sku_column_name=PRODUCTS_TABLE_SKU_COLUMN_NAME,
            url_column_name=PRODUCTS_TABLE_URL_COLUMN_NAME
        )

    @staticmethod
    def insert_values_string():
        return '({barcode_column_name}, {sku_column_name}, {url_column_name}) '.format(
            barcode_column_name=PRODUCTS_TABLE_BARCODE_COLUMN_NAME,
            sku_column_name=PRODUCTS_TABLE_SKU_COLUMN_NAME,
            url_column_name=PRODUCTS_TABLE_URL_COLUMN_NAME
        )

    def insert_values_to_string(self):
        return '({barcode}, {sku}, {url})'.format(
            barcode=("'" + self.barcode + "'"),
            sku=("'" + self.sku + "'"),
            url=("'" + self.url + "'")
        )
    
    @staticmethod
    def get_excel_data_header():
        return ['Штрих-Код', 'SKU', 'URL-адрес']

    def __iter__(self):
        return iter([self.barcode, self.sku, self.url])
