from database.mydataclasses import Product
from .exceptions import IncorrectInputException


class Handler:
    def __init__(self, text):
        if not text:
            raise IncorrectInputException('сообщение не содержит текста')
        lines = [line.strip() for line in text.split('\n') if line != '\n' and line]
        if len(lines) < 3:
            raise IncorrectInputException('количество строк меньше трёх')

        barcode = lines[0]
        sku = lines[1]
        self.products = []
        for line in lines[2:]:
            self.products.append(Product(
                barcode=barcode,
                sku=sku,
                url=line
            ))
