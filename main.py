#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import Updater
import logging,pickle
from random import choice
from manager import manager
from datetime import datetime

man = manager()
haukkumanimi = ["apina","fagem","gay","homo","fagum","tyhmä","retard","kivi","kahva","jutsku","peelo"]


def load_insults():
    file = open("insult.pc",'rb')
    f = d = pickle.load(file)
    file.close()
    print("loaded insults")
    return f

#insults = load_insults()

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

def get_insult(name,msg):
    print(name,msg)
    i1,i2 = [], []
    for x in insults:
        if x[0]:
            i1.append(x)
        else:
            i2.append(x)
    if name:
        r = choice(i1)
        r = r[1].replace("-name-",msg)
        return r
    else:
        r = choice(i2)
        r = r[1]
        return r

def insult(bot,update):
    name = update.message.from_user.username
    id = update.message.chat_id
    text = update.message.text
    text = text.replace("/kiusua","")
    if text == "":
        print(11)
        r = get_insult(False,"")
        bot.sendMessage(id,r)
    else:
        print(22)
        r = get_insult(True,text)
        bot.sendMessage(id,r)

def new_insult(bot,update):
    name = update.message.from_user.username
    id = update.message.chat_id
    text = update.message.text
    text = text.replace("/new_insult","")
    text = text[1:]
    if text != "":
        if "-name-" in text:
            print(1)
            print(text)
            x = (True,text)
            print(x)
            insults.append(x)
            save_insult(insults)
        else:
            print(2)
            print(text)
            x = (False,text)
            print(x)
            insults.append(x)
            save_insult(insults)

        bot.sendMessage(id,"Insult added.")
    else:
        bot.sendMessage(id,"Tyhjä lause vitun retardi.")

def reactio(bot,update):
    name = update.message.from_user.username
    id = update.message.chat_id

    print(name + " - reactio")
    if name not in man.cd_list.keys():
        man.cd_list[name] = datetime.now()
        r = man.get_img("r")
        if type(r) is not None: bot.sendPhoto(id,r)
        else: bot.sendMessage(id,"kaalilaatikko")

    else:
        if man.check_cd(name,60):
            man.cd_list[name] = datetime.now()
            r = man.get_img("r")
            if type(r) is not None: bot.sendPhoto(id,r)
            else: bot.sendMessage(id,"kaalilaatikko")
        else:
            bot.sendMessage(id,"Olet failannut muistaa cooldownin {0} kertaa. OOTKO {1}"
                                .format(man.cd_fail[name],choice(haukkumanimi).upper()))

def kuva(bot,update):
    name = update.message.from_user.username
    id = update.message.chat_id

    print(name + " - kuva")
    if name not in man.cd_list.keys():
        man.cd_list[name] = datetime.now()
        r = man.get_img("k")
        if type(r) is not None: bot.sendPhoto(id,r)
        else: bot.sendMessage(id,"kaalilaatikko")

    else:
        if man.check_cd(name,60):
            man.cd_list[name] = datetime.now()
            r = man.get_img("k")
            if type(r) is not None: bot.sendPhoto(id,r)
            else: bot.sendMessage(id,"kaalilaatikko")
        else:
            bot.sendMessage(id,"Olet failannut muistaa cooldownin {0} kertaa. OOTKO {1}"
                                .format(man.cd_fail[name],choice(haukkumanimi).upper()))

def jutku(bot,update):
    if "jew" in update.message.text or "jutku" in update.message.text:
        if "jutku" not in man.cd_list.keys():
            man.cd_list["jutku"] = datetime.now()
            id = update.message.chat_id
            r = man.get_img("j")
            bot.sendPhoto(id,r)
        else:
            if man.check_cd("jutku",30):
                man.cd_list["jutku"] = datetime.now()
                id = update.message.chat_id
                r = man.get_img("j")
                bot.sendPhoto(id,r)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    updater = Updater(man.settings["authkey"])
    dp = updater.dispatcher

    dp.addTelegramCommandHandler("reactio", reactio)
    dp.addTelegramCommandHandler("kuva", kuva)
    #dp.addTelegramCommandHandler("kiusua", insult)
    #dp.addTelegramCommandHandler("new_insult", new_insult)
    dp.addTelegramMessageHandler(jutku)

    dp.addErrorHandler(error)
    update_queue = updater.start_polling(poll_interval=0.1, timeout=10)

    while True:
        try:
            text = input()
        except NameError:
            text = input()

        # Gracefully stop the event handler
        if text == 'stop':
            updater.stop()
            break

        # else, put the text into the update queue to be handled by our handlers
        elif len(text) > 0:
            update_queue.put(text)

if __name__ == '__main__':
    main()
