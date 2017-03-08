# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler
import random
from emoji import emojize
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    update.message.reply_text('Hello World!')

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def dice(bot, update, args):
    num_dice = int(args[0]) if len(args)>0 else 4
    dice_res = u''
    dice_val = 0
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

    dice_res+="({})".format(dice_val)
    bot.sendMessage(chat_id=update.message.chat_id, text=dice_res)

updater = Updater('330715814:AAFa4y4MFhfoU7yIrS5owBfuMkpxsLKjmaQ')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('dice', dice, pass_args=True))

updater.start_polling()
updater.idle()
