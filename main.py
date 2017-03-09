# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import random
from emoji import emojize
import datetime
import socket
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
from google.cloud import datastore
from flask import Flask, request
import util

app = Flask(__name__)

TOKEN = '330715814:AAFa4y4MFhfoU7yIrS5owBfuMkpxsLKjmaQ'

@app.route('/')
def index():
    return ".", 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/HOOK', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = Update.de_json(request.get_json(force=True), bot)
        updater.dispatcher.process_update(update)
    return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    updater.dispatcher.add_handler(CommandHandler('newchar', newchar))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('dice', dice, pass_args=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, main_filter))
    s = updater.bot.setWebhook('https://fudgerpgbot.appspot.com/HOOK')
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

# CONSTANTS
STATE_CHAT = 0
STATE_CREATE_CHAR = 10

players = {}
class Player:
    id = 0
    name = ""
    state = STATE_CHAT

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.state = STATE_CHAT

    def message_from_self(self, message):
        return u"You say: \"{}\"".format(message)

    def message_from(self, message):
        return u"{} says: \"{}\"".format(self.name, message)


# MAIN FILTER
def main_filter(bot, update):
    current_player = players[update.message.from_user.id]

    if current_player.state == STATE_CHAT:
        for player in players.values():
            if player.id == current_player.id:
                bot.sendMessage(chat_id=player.id, text=player.message_from_self(update.message.text))
            else:
                bot.sendMessage(chat_id=player.id, text=player.message_from(update.message.text))

    elif current_player.state == STATE_CREATE_CHAR:
        message = update.message.text

        if message == "done":
            current_player.state=STATE_CHAT
            bot.sendMessage(chat_id=current_player.id, text="Done.", reply_markup=ReplyKeyboardRemove())


# COMMANDS START HERE
def start(bot, update):
    player_id = update.message.from_user.id
    player_name = update.message.from_user.first_name
    players[player_id] = Player(player_id, player_name)

    update.message.reply_text('Welcome {}'.format(player_name))

def newchar(bot, update):
    current_player = players[update.message.from_user.id]
    current_player.state = STATE_CREATE_CHAR
    button_list = [
        KeyboardButton("add"),
        KeyboardButton("remove"),
        KeyboardButton("skills"),
        KeyboardButton("done")
    ]
    reply_markup = ReplyKeyboardMarkup(util.build_menu(button_list, n_cols=2))
    bot.sendMessage(chat_id=update.message.chat_id, text="Create your char:", reply_markup=reply_markup)

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def dice(bot, update, args):
    text = u''

    dice_res = u''
    dice_val = 0
    num_dice = int(args[0]) if len(args)>0 else 4
    for d in range(num_dice):
        value = random.randint(1,3)
        if value==1:
            dice_res+=emojize(":heavy_plus_sign:", use_aliases=True)
            dice_val+=1
        elif value==2:
            dice_res+=emojize(":white_medium_square:", use_aliases=True)
        elif value==3:
            dice_res+=emojize(":heavy_minus_sign:", use_aliases=True)
            dice_val-=1

    text = u"{} rolled {}({})".format(update.message.from_user.first_name, dice_res, dice_val)
    bot.sendMessage(chat_id=update.message.chat_id, text=text)

global updater
updater = Updater(TOKEN)
