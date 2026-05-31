import os
from telebot import TeleBot

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
bot = TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, "⚡ " + message.text)

bot.infinity_polling()
