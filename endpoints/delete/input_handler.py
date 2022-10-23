from .exceptions import IncorrectInputException


class Handler:
    def __init__(self, text):
        if not text:
            raise IncorrectInputException('сообщение не содержит текста')
