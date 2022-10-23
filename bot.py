from telebot import TeleBot

from config import TOKEN
from endpoints.add.add import add_endpoint_impl
from endpoints.list.list import list_endpoint_impl
from endpoints.delete.delete import delete_endpoint_impl
from endpoints.parse.parse import parse_endpoint_impl

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['add'])
def add_endpoint(message):
    add_endpoint_impl(bot=bot, message=message)


@bot.message_handler(commands=['list'])
def list_endpoint(message):
    list_endpoint_impl(bot=bot, message=message)


@bot.message_handler(commands=['delete'])
def delete_endpoint(message):
    delete_endpoint_impl(bot=bot, message=message)


@bot.message_handler(commands=['parse'])
def parse_endpoint(message):
    parse_endpoint_impl(bot=bot, message=message)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    main()
