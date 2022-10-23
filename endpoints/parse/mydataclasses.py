from dataclasses import dataclass


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
    competitor: str
    default_price: Price
    promo_price: Price
