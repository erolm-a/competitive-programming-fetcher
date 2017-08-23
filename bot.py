#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright by Enrico "erolm_a" Trombetta
#
# This file is part of Competitive Programming Fetcher
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job

import fetcher
import logging
import time
import conf
import database
from datetime import datetime

db = database.Database()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

help_string = "Questo bot estrae un testo a caso dal CMS e da altri fonti. I testi vengono estratti alle 0:00 di ogni giorno e sono automaticamente appesi"
        
all_chat_ids = set()

def send_fetch(bot, chat_id):
    bot.send_message(chat_id=chat_id, text="Dal CMS:\n{}".
            format(fetcher.fetch_OII()))

def broadcast(bot, job):
    for chat_id in db.get_chat_list():
        fetch(bot, chat_id) 
    
def start(bot, update):
    chat_id = update.message.chat_id
    update.message.reply_text(help_string)
    db.register_chat_id(chat_id)
    db.flush()
    send_fetch(bot, chat_id)

def help(bot, update):
    update.message.reply_text(help_string)
    
def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def main():
    global bot
    updater = Updater(conf.SECRET_TOKEN)
    job_queue = updater.job_queue
    
    now = datetime.now()
    seconds_to_midnight = (now.replace(hour=23, minute=59, second=59, microsecond=0) - now).total_seconds()
    print("Secondi a mezzanotte: {}".format(seconds_to_midnight))

    fetch_job = Job(broadcast, 86400)
    job_queue.put(fetch_job, next_t=seconds_to_midnight)
    
    # get the dispatcher
    dp = updater.dispatcher
    bot = updater.bot
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    try:
        main()
    finally:
        exit()
