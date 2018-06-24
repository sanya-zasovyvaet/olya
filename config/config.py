# -*- coding: utf-8 -*-
from config.tokens import *
import vk
import os

# vk config
group_name = 'suicidegirls'
session = vk.Session(access_token=vk_token)
vk_api = vk.API(session)

# For proxy connection
REQUEST_KWARGS = {
    'proxy_url': 'socks5://199.247.14.47:10080',
    'urllib3_proxy_kwargs': {
        'username': 'tgfree_user',
        'password': 'laip3Ez6',
    }
}

# TODO change it to name of your bot
bot_name = u'Olenka_bot'

# Dirs and file names
PROJECT_DIR = os.getcwd() + '\\'
MESSAGES_DIR = PROJECT_DIR + 'messages\\'
STICKERS_DIR = PROJECT_DIR + 'stickers\\'
JOKES_DBNAME = PROJECT_DIR + 'db\\jokes.db'
BUGURT_DBNAME = PROJECT_DIR + 'db\\bugurt.db'

# Creating directories if they not exist
for directory in MESSAGES_DIR, STICKERS_DIR:
    try:
        os.stat(directory)
    except FileNotFoundError:
        os.mkdir(directory)
