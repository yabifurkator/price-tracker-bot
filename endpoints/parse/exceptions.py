
class FailedParseException(Exception):
    def __init__(self, reason, url):
        self.reason = reason
        self.url = url

        message = (
            'Ошибка структурного анализа страницы.\n'
            'Причина: ' + reason + '.\n'
            'URL-адрес: ' + url
        )
        super().__init__(message)
