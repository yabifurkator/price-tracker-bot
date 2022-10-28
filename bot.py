from telebot import TeleBot

from config import TOKEN
from endpoints.add.add import add_endpoint_impl
from endpoints.list.list import list_endpoint_impl
from endpoints.delete.delete import delete_endpoint_impl
from endpoints.parse.parse import parse_endpoint_impl

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


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
