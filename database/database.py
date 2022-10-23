import psycopg2
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION

from database.exceptions import \
    FailedToInsertException, \
    FailedToSelectException, \
    FailedToDeleteException

from config import \
    DATABASE_NAME, \
    DATABASE_USER_NAME, \
    DATABASE_USER_PASSWORD, \
    DATABASE_HOST, \
    DATABASE_PORT


class DataBaseConnector:
    @staticmethod
    def get_connection():
        connection = psycopg2.connect(
            dbname=DATABASE_NAME,
            user=DATABASE_USER_NAME,
            password=DATABASE_USER_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT
        )
        connection.autocommit = True
        return connection

    @staticmethod
    def execute(connection, sql_request):
        cursor = connection.cursor()
        cursor.execute(sql_request)
        return cursor

    @staticmethod
    def insert(connection, sql_request):
        try:
            DataBaseConnector.execute(connection, sql_request)
        except errors.lookup(UNIQUE_VIOLATION):
            raise FailedToInsertException('ошибка уникальности')

    @staticmethod
    def select(connection, sql_request):
        cursor = DataBaseConnector.execute(connection, sql_request)
        cursor_fetch = cursor.fetchall()
        if len(cursor_fetch) == 0:
            raise FailedToSelectException('не было найдено подходящих записей')
        return cursor_fetch

    @staticmethod
    def delete(connection, sql_request):
        cursor = DataBaseConnector.execute(connection, sql_request)
        if cursor.rowcount == 0:
            raise FailedToDeleteException('не было найдено подходящих записей')
