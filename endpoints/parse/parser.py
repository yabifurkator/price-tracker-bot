from enum import Enum

from .exceptions import \
    UnknownCompetitorException, \
    ParseException

from .mydataclasses import \
    Competitor, \
    ParseData, \
    Price

from .parsers import \
    ulybka_radugi_parser, \
    novex_parser, \
    podrugka_parser, \
    fortuna_parser, \
    parfum_lider_parser, \
    optima_parser, \
    wbc_parser, \
    belfeya_parser, \
    kalina_parser, \
    okeandra_parser, \
    zapovednaya_polyana_parser, \
    victoria_parser, \
    vprok_parser, \
    sem_dney_parser, \
    magnit_parser, \
    magnit_cosmetic_parser


class Competitors(Enum):
    ULYBKA_RADUGI = Competitor(
        url='https://www.r-ulybka.ru/',
        name='Улыбка радуги',
        parser=ulybka_radugi_parser
    )
    NOVEX = Competitor(
        url='https://novex.ru/',
        name='Novex',
        parser=novex_parser
    )
    PODRYGKA = Competitor(
        url='https://www.podrygka.ru/',
        name='Подружка',
        parser=podrugka_parser
    )
    FORTUNA = Competitor(
        url='https://fortuna99.ru/',
        name='Фортуна',
        parser=fortuna_parser
    )
    PARFUM_LIDER = Competitor(
        url='https://www.parfum-lider.ru/',
        name='Парфюм-Лидер',
        parser=parfum_lider_parser
    )
    OPTIMA = Competitor(
        url='https://ioptima.ru/',
        name='Оптима',
        parser=optima_parser
    )
    WBC = Competitor(
        url='https://www.wbc-c.ru/',
        name='wbc',
        parser=wbc_parser
    )
    BELFEYA = Competitor(
        url='https://belfeya.ru/',
        name='Белфея',
        parser=belfeya_parser
    )
    KALINA = Competitor(
        url='http://kalinamag.ru/',
        name='Калина',
        parser=kalina_parser
    )
    OKEANDRA = Competitor(
        url='https://okeandra.ru/',
        name='Океандра',
        parser=okeandra_parser
    )
    ZAPOVEDNAYA_POLYANA = Competitor(
        url='https://zapovednaya-polyana.ru/',
        name='Заповедная Поляна',
        parser=zapovednaya_polyana_parser
    )
    VICTORIA = Competitor(
        url='https://www.shop.vic-spb.ru/',
        name='Виктория',
        parser=victoria_parser
    )
    VPROK = Competitor(
        url='https://www.tkvprok.ru/',
        name='Впрок',
        parser=vprok_parser
    )
    SEM_DNEY = Competitor(
        url='https://ts-7dney.ru/',
        name='Семь дней',
        parser=sem_dney_parser
    )
    MAGNIT = Competitor(
        url='https://magnit.ru/',
        name='Магнит',
        parser=magnit_parser
    )
    MAGNIT_COSMETIC = Competitor(
        url='https://magnitcosmetic.ru/',
        name='Магнит Косметик',
        parser=magnit_cosmetic_parser
    )


def define_competitor(url):
    for competitor in Competitors:
        competitor_dataclass: Competitor = competitor.value
        if competitor_dataclass.url in url:
            return competitor.value
    return None


def parse(url):
    competitor: Competitor = define_competitor(url)
    if competitor is None:
        raise UnknownCompetitorException(url=url)

    default_price, promo_price = competitor.parser(url)

    parse_data = ParseData(
        competitor_name=competitor.name,
        default_price=default_price,
        promo_price=promo_price
    )
    return parse_data
