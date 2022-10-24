from dataclasses import dataclass

from config import NONE_PRICE_PLACEHOLDER


@dataclass
class PriceLine:
    barcode: str
    sku: str
    competitor_name: str
    date: str
    default_price: str
    promo_price: str
    url: str

    @staticmethod
    def get_excel_data_header():
        return [
            'Штрих-Код',
            'SKU',
            'Конкурент',
            'Дата',
            'Розничная цена',
            'Акционная цена',
            'URL-адрес'
        ]

    def to_excel_line(self):
        return [
            self.barcode,
            self.sku,
            self.competitor_name,
            self.date,
            self.default_price,
            self.promo_price,
            self.url
        ]


@dataclass
class ErrorLine:
    barcode: str
    sku: str
    date: str
    reason: str
    url: str

    @staticmethod
    def get_excel_data_header():
        return ['Штрих-Код', 'SKU', 'Дата', 'Причина', 'URL-адрес']

    def to_excel_line(self):
        return [self.barcode, self.sku, self.date, self.reason, self.url]


@dataclass
class Competitor:
    url: str
    name: str
    parser: callable


@dataclass
class Price:
    integer_part: int
    fractional_part: int

    def __str__(self, part_separator='.'):
        integer_part_str = str(self.integer_part)
        if self.fractional_part < 10:
            fractional_part_str = '0{}'.format(self.fractional_part)
        else:
            fractional_part_str = str(self.fractional_part)
        return integer_part_str + part_separator + fractional_part_str


@dataclass
class ParseData:
    competitor_name: str
    default_price: Price
    promo_price: Price

    @staticmethod
    def price_to_string(price: Price):
        if price is None:
            return NONE_PRICE_PLACEHOLDER
        return str(price)
