
class InputException(Exception):
    pass


class IncorrectInputException(InputException):
    def __init__(self, reason):
        message = 'Неверный формат входных данных.\nПричина: ' + reason + '.'
        super().__init__(message)
