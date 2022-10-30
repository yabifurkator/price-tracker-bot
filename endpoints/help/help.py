from telebot import TeleBot

from endpoints.help import HELP_MESSAGE


def help_endpoint_impl(bot: TeleBot, message):
    text_to_send = HELP_MESSAGE
    bot.reply_to(message, text=text_to_send)
