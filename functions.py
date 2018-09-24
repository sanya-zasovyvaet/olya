# -*- coding: utf-8 -*-
import sqlite3
import random
import re

from config.arrays import *
from config.config import *
from parse_utils.db import Db
from parse_utils.gen import Generator
from parse_utils.parse import Parser
from parse_utils.sql import Sql
from parse_utils.rnd import Rnd


def bugurt(bot, update):
    string = ''
    while len(string) < 3:
        count = random.randint(1, 5)
        db = Db(sqlite3.connect(BUGURT_DBNAME), Sql())
        generator = Generator(BUGURT_DBNAME, db, Rnd())
        for i in range(0, count):
            string += generator.generate()
            string += '\n@\n'
    string = '\n' + string[:-3] + '\n'
    update.message.reply_text(string)


def get_joke():
    word_separator = ' '
    string = ''
    while len(string) < 2:
        count = 1
        db = Db(sqlite3.connect(JOKES_DBNAME), Sql())
        generator = Generator(JOKES_DBNAME, db, Rnd())
        for i in range(0, count):
            string += generator.generate(word_separator)
    return string


def get_message(update):
    word_separator = ' '
    string = ''
    chat_id = str(update.message.chat.id)
    db_name = MESSAGES_DIR + chat_id + '.db'
    while len(string) < 2:
        db = Db(sqlite3.connect(db_name), Sql())
        generator = Generator(db_name, db, Rnd())
        string += generator.generate(word_separator)
    return string


def get_sticker(bot, update):
    reply_to = ''
    if update.message.reply_to_message is not None:
        reply_to = update.message.reply_to_message.from_user.username
    if update.message.reply_to_message is not None and reply_to == bot_name:
        chat_id = str(update.message.chat.id)
        stickers_file_name = STICKERS_DIR + chat_id
        stickers_list = []

        try:
            with open(stickers_file_name) as stickers_file:
                stickers_list = stickers_file.readlines()
        except FileNotFoundError:
            # Create stickers file if it not exists
            open(stickers_file_name, 'w').close()

        sticker_id = update.message.sticker.file_id
        if not sticker_id + '\n' in stickers_list:
            with open(stickers_file_name, 'w') as stickers_file:
                stickers_file.write(sticker_id + '\n')

        # Read stickers file to load new added sticker
        with open(stickers_file_name) as stickers_file:
            stickers_list = stickers_file.readlines()

        if stickers_list:
            update.message.reply_sticker(random.choice(stickers_list)[:-1])


def joke(bot, update):
    update.message.reply_text(get_joke())


def name_in(message):
    txt = re.sub(r'^[\s\W]*|[^\w ]|\s(?=[\W\s]|$)(?u)', '', message.lower())
    for word in txt.split():
        if word in names.split():
            return True
    return False


def reply_to_message(bot, update):
    save_message(update)
    reply_to = None
    if update.message.reply_to_message is not None:
            reply_to = update.message.reply_to_message.from_user.username
    if name_in(update.message.text) or reply_to == bot_name:
        if u'или' in update.message.text.split():
            redata = re.compile(re.escape(u'ты'), re.IGNORECASE)
            update.message.text = redata.sub(u'я', update.message.text)
            out = []
            for words in update.message.text.replace(u'?', u'').split(u','):
                for word in words.split(u'или'):
                    if not name_in(word):
                        out.append(word.strip(u' '))
            if not len(out):
                update.message.reply_text(u'что-то не так')
            else:
                update.message.reply_text(random.choice(out))
        else:
            send_message(bot, update)


def roll(bot, update):
    out = ''
    for i in range(6):
        out += str(random.randint(0, 9))
    update.message.reply_text(out)


def save_message(update):
    if not update.message.text.startswith('/')\
            and not name_in(update.message.text)\
            and u'http' not in update.message.text:
        chat_id = str(update.message.chat.id)
        db_name = MESSAGES_DIR + chat_id + '.db'
        db = Db(sqlite3.connect(db_name), Sql())
        db.setup(depth=2)

        txt = update.message.text.replace(u'\n', u' ').lower() + '\n'
        Parser(db_name, db).parse(txt)


def send_help(bot, update):
    help_text = '''
Ну кароч смотри...

Я отзываюсь на свое имя (ну там Оля, Оляшка, эй Оль...)

Запоминаю то, что ты мне говоришь, и говорю на твоем же языке.

А еще я помню и шлю стикеры, которые ты мне шлешь. \
Ну и те, что мне другие люди шлют, так что не удивляйся стикерам с Гитлерами и всякому такому.

Если ты безвольная тряпка и не можешь сам что-то решить, то можешь спросить у меня! \
Напиши ченить типа "Синий, зеленый или я мудак?" и я решу за тебя. Только обязательно с "или", а то я тебя не пойму.
'''
    update.message.reply_text(text=help_text)


def send_message(bot, update):
    chat_id = str(update.message.chat.id)
    stickers_file_name = STICKERS_DIR + chat_id
    stickers_file_exists = os.path.isfile(stickers_file_name)
    if not random.randint(0, 3) and stickers_file_exists:
        stickers = open(stickers_file_name, 'r').readlines()
        update.message.reply_sticker(random.choice(stickers)[:-1])
    else:
        message_out = get_message(update)
        update.message.reply_text(message_out)


def spicy(bot, update):
    group_id = vk_api.groups.getById(group_id=group_name)[0]['gid']
    album_id = random.choice(vk_api.photos.getAlbums(owner_id=-group_id))['aid']
    link = random.choice(vk_api.photos.get(owner_id=-group_id, album_id=album_id))['src_xxbig']
    bot.send_photo(chat_id=update.message.chat.id, photo=link)


def start(bot, update):
    update.message.reply_text(random.choice(hellos))
