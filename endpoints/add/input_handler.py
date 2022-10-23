from database.mydataclasses import Product
from .exceptions import IncorrectInputException


class Handler:
    def __init__(self, text):
        if not text:
            raise IncorrectInputException('сообщение не содержит текста')
        lines = [line.strip() for line in text.split('\n')]
        if len(lines) != 3:
            raise IncorrectInputException('количество строк не равно трём')

        self.products_table_data_class = Product(
            barcode=lines[0],
            sku=lines[1],
            url=lines[2]
        )
