from telebot import TeleBot
import schedule
import threading
import time

from config import \
    TOKEN, \
    TELEGRAM_ID_LIST_FILE_PATH
from endpoints.add.add import add_endpoint_impl
from endpoints.list.list import list_endpoint_impl
from endpoints.delete.delete import delete_endpoint_impl
from endpoints.parse.parse import parse_endpoint_impl
from endpoints.get.get import get_endpoint_impl
from schedule_tools import schedule_func

bot = TeleBot(token=TOKEN)


def add_endpoint(message):
    add_endpoint_impl(bot=bot, message=message)


def list_endpoint(message):
    list_endpoint_impl(bot=bot, message=message)


def delete_endpoint(message):
    delete_endpoint_impl(bot=bot, message=message)


def parse_endpoint(message):
    parse_endpoint_impl(bot=bot, message=message)


@bot.message_handler(commands=['get'])
def get_endpoint(message):
    get_endpoint_impl(bot=bot, message=message)


def check_user(user_telegram_id):
    with open(TELEGRAM_ID_LIST_FILE_PATH, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            if line.strip().split()[0] == str(user_telegram_id):
                return True
        return False


@bot.message_handler(content_types=['text'])
def text_endpoint(message):
    try:
        telegram_id = message.from_user.id
        if not check_user(telegram_id):
            text_to_send = (
                'Ошибка: Вас нет в базе данных.\n'
                'Обратитесь к системному администратору.\n\n'
                'Ваш TelegramID: {}'.format(telegram_id)
            )
            bot.reply_to(message=message, text=text_to_send)
            return

        match message.text:
            case '/add':
                add_endpoint(message=message)
            case '/list':
                list_endpoint(message=message)
            case '/delete':
                delete_endpoint(message=message)
            case '/parse':
                parse_endpoint(message=message)
            case '/get':
                get_endpoint(message=message)
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))


def run_bot():
    bot.infinity_polling()


def run_schedule():
    schedule.every().monday.at('00:00').do(schedule_func)
    while True:
        schedule.run_pending()
        time.sleep(1)


def main():
    thread1 = threading.Thread(target=run_bot)
    thread2 = threading.Thread(target=run_schedule)

    thread1.start()
    thread2.start()


if __name__ == '__main__':
    main()
