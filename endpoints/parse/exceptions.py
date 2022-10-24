
class ParseException(Exception):
    def __init__(self, reason, url):
        self.reason = reason
        self.url = url

        message = (
            'Ошибка структурного анализа страницы.\n'
            'Причина: ' + reason + '.\n'
            'URL-адрес: ' + url
        )
        super().__init__(message)


class UnknownCompetitorException(ParseException):
    def __init__(self, url):
        super().__init__(
            reason='URL-адрес не совпадает ни с одним URL-адресом конкурента',
            url=url
        )


class RequestException(ParseException):
    def __init__(self, url):
        super().__init__(
            reason='не удалось сделать запрос на указанный URL-адрес',
            url=url
        )


class UnexpectedPageStructureException(ParseException):
    def __init__(self, url):
        super().__init__(
            reason='неожиданная структура страницы',
            url=url
        )


class FailedToGetJsonException(ParseException):
    def __init__(self, url):
        super().__init__(
            reason='не удалось получить JSON объект',
            url=url
        )


class ProductNotAvailableException(ParseException):
    def __init__(self, url):
        super().__init__(
            reason='не удалось получить актуальную цену товара, возможно его нет в наличии',
            url=url
        )
