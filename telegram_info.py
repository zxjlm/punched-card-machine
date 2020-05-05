# -*- coding:utf-8 -*-
__author__ = 'harumonia'

from telegram.ext import CommandHandler
from telegram.ext import Updater

from secure import bot_token
from settings import proxy


class TelegramHandler:
    updater = Updater(bot_token, use_context=True, request_kwargs={'proxy_url': proxy})

    def __init__(self, r):
        self.r = r

    def start_query(self):
        dispatcher = self.updater.dispatcher

        def query(update, context):
            sl = [str(k) + ':' + str(v) for k, v in self.r.hgetall('success').items()]
            s = '\n '.join(sl[::-1][:5])
            context.bot.send_message(chat_id=update.effective_chat.id, text='最新的5条:'+s)

        start_handler = CommandHandler('query', query)
        dispatcher.add_handler(start_handler)

        self.updater.start_polling()
