import datetime

import telegram

from ..config import Config

config = Config()

bot = telegram.Bot(config.telegram_token)
chat_id = bot.get_updates()[-1].message.chat_id
bot.send_message(chat_id, 'Hello, <b>World!</b>', parse_mode='HTML')
bot.send_message(chat_id, 'Hello, *Again!*', parse_mode='MARKDOWN')