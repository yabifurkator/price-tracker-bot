
class DataBaseException(Exception):
    pass


class FailedToInsertException(DataBaseException):
    def __init__(self, reason):
        message = "Не удалось добавить новую запись.\nПричина: " + reason + '.'
        super().__init__(message)


class FailedToSelectException(DataBaseException):
    def __init__(self, reason):
        message = 'Не удалось получить выборку записей.\nПричина: ' + reason + '.'
        super().__init__(message)


class FailedToDeleteException(DataBaseException):
    def __init__(self, reason):
        message = "Не удалось удалить запись.\nПричина: " + reason + '.'
        super().__init__(message)
