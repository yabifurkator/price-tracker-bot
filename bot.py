from telebot import TeleBot
import schedule
import threading
import time

from config import TOKEN
from endpoints.add.add import add_endpoint_impl
from endpoints.list.list import list_endpoint_impl
from endpoints.delete.delete import delete_endpoint_impl
from endpoints.parse.parse import parse_endpoint_impl
from endpoints.get.get import get_endpoint_impl
from schedule_tools import schedule_func

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['add'])
def add_endpoint(message):
    try:
        add_endpoint_impl(bot=bot, message=message)
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))


@bot.message_handler(commands=['list'])
def list_endpoint(message):
    try:
        list_endpoint_impl(bot=bot, message=message)
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))


@bot.message_handler(commands=['delete'])
def delete_endpoint(message):
    try:
        delete_endpoint_impl(bot=bot, message=message)
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))


@bot.message_handler(commands=['parse'])
def parse_endpoint(message):
    try:
        parse_endpoint_impl(bot=bot, message=message)
    except Exception as ex:
        bot.send_message(chat_id=message.chat.id, text=str(ex))


@bot.message_handler(commands=['get'])
def get_endpoint(message):
    try:
        get_endpoint_impl(bot=bot, message=message)
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
