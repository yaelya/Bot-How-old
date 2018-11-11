import logging
import requests
NEEDLE = "(age&#160;"
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

import bot_settings

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.BOT_TOKEN)
dispatcher = updater.dispatcher


def start(bot, update):
    chat_id = update.message.chat_id
    logger.info(f"> Start chat #{chat_id}")
    bot.send_message(chat_id=chat_id, text="Hello! Enter a celebrity name and I'll tell you her age!")


def respond(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {text!r}")
    response = how_old_is(text)
    if not response:
        response = f"Sorry, I don't know any {text}"

    bot.send_message(chat_id=update.message.chat_id, text=response)

def how_old_is(name):
    r = requests.get("https://en.wikipedia.org/wiki/" + name)
    a = r.text.find(NEEDLE)
    if a == -1:
        return None
    return int(r.text[a + len(NEEDLE):r.text.find(")", a)])


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

how_old_is_handler = CommandHandler('howoldis',how_old_is)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, respond)
dispatcher.add_handler(echo_handler)

logger.info("Start polling")
updater.start_polling()