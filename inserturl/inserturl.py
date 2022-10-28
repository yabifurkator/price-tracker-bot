from database.database import DataBaseConnector
from database.exceptions import DataBaseException
from database.mydataclasses import Product
from config import PRODUCTS_TABLE_NAME


def insert(url_file_path):
    connection = DataBaseConnector.get_connection()

    url_file = open(url_file_path, 'r')
    for line in url_file:
        if line == '\n':
            continue

        dataclass = Product(barcode='barcode', sku='sku', url=line.strip())
        sql_request = (
            'INSERT INTO {} '.format(PRODUCTS_TABLE_NAME) +
            dataclass.insert_values_string() +
            ' VALUES {}'.format(dataclass.insert_values_to_string())

        )
        try:
            DataBaseConnector.insert(connection=connection, sql_request=sql_request)
        except DataBaseException as ex:
            print(ex)


def main():
    insert('url.txt')
    pass


if __name__ == '__main__':
    main()
