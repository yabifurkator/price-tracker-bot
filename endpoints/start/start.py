from telebot import TeleBot

from endpoints.help import HELP_MESSAGE


def start_endpoint_impl(bot: TeleBot, message):
    text_to_send = (
        'Старт!\n'
    )
    bot.reply_to(message=message, text=text_to_send)

    text_to_send = HELP_MESSAGE
    bot.send_message(chat_id=message.chat.id, text=text_to_send)
