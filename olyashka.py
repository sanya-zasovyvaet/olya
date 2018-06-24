#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from functions import *


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(
        bot_token,
        request_kwargs=REQUEST_KWARGS
    )
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("bugurt", bugurt))
    dp.add_handler(CommandHandler("roll", roll))
    dp.add_handler(CommandHandler("spicy", spicy))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CommandHandler("help", send_help))
    dp.add_handler(MessageHandler(Filters.text, reply_to_message))
    dp.add_handler(MessageHandler(Filters.sticker, get_sticker))
    dp.add_error_handler(error)

    updater.start_polling(poll_interval=3.0, timeout=0)
    updater.idle()


if __name__ == '__main__':
    main()
