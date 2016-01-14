#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import Updater
import logging,pickle,datetime,json
from random import choice
from os import listdir
from os.path import isfile, join

haukkumanimi = ["apina","fagem","gay","homo","fagum","tyhmä","retard","kivi","kahva","jutsku","peelo"]

#lataa asetukset
with open("settings.json","r") as f:
    try:
        settings = json.load(f)
    except ValueError:
        settings = {}
        print("Error loading settings")

with open("cd_fail.json","r") as f:
    try:
        cd_fail = json.load(f)
    except ValueError:
        cd_fail = {}
        print("Error loading settings")

def save_insult(savefile):
    with open('insult.pc', 'wb') as handle:
                pickle.dump(savefile, handle)
    print("saved asd")

def load_insults():
    file = open("insult.pc",'rb')
    f = d = pickle.load(file)
    file.close()
    print("loaded insults")
    return f

insults = load_insults()

mypath = "kuva"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print("loaded " + str(len(onlyfiles) +1) + " files")

mypath2 = "kuvaR"
onlyfilesR = [f for f in listdir(mypath2) if isfile(join(mypath2, f))]
print("loaded " + str(len(onlyfilesR) +1) + " files")

users = {}

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



def reactio(bot,update):

    path = "kuva/" + choice(onlyfiles)

    name = update.message.from_user.username
    id = update.message.chat_id
    text = update.message.text
    time = datetime.datetime.now()

    print(name + " - reactio")
    if name not in users.keys():
        print("post 1")
        users[name] = datetime.datetime.now() + datetime.timedelta(minutes=1)
        kuva = open(path,"rb")
        bot.sendPhoto(id,kuva)
        kuva.close()

    else:
        print(users[name],time)
        if time > users[name]:
            kuva = open(path,"rb")
            bot.sendPhoto(id,kuva)
            kuva.close()
            users[name] = datetime.datetime.now() + datetime.timedelta(minutes=1)
        else:
            if name not in cd_fail.keys():
                cd_fail[name] = 1
            else:
                cd_fail[name] += 1
                bot.sendMessage(id,"Olet failannut muistaa cooldownin {0} kertaa. OOTKO {1}"
                                .format(cd_fail[name],choice(haukkumanimi).upper()))
                with open('cd_fail.json', 'w') as outfile:
                    json.dump(cd_fail, outfile)
            print(name + " cooldown")

def kuva(bot,update):

    path = "kuvaR/" + choice(onlyfilesR)

    name = update.message.from_user.username
    id = update.message.chat_id
    text = update.message.text
    time = datetime.datetime.now()

    print(name + " - kuva")
    if name not in users.keys():
        print("post 1")
        users[name] = datetime.datetime.now() + datetime.timedelta(minutes=1)
        kuva = open(path,"rb")
        bot.sendPhoto(id,kuva)
        kuva.close()

    else:
        print(users[name],time)
        if time > users[name]:
            kuva = open(path,"rb")
            bot.sendPhoto(id,kuva)
            kuva.close()
            users[name] = datetime.datetime.now() + datetime.timedelta(minutes=1)
        else:
            if name not in cd_fail.keys(): cd_fail[name] = 1
            else: cd_fail[name] += 1
            bot.sendMessage(id,"Olet failannut muistaa cooldownin {0} kertaa. ootko {1}"
                                .format(cd_fail[name],choice(haukkumanimi).upper()))
            with open('cd_fail.json', 'w') as outfile:
                    json.dump(cd_fail, outfile)
            print(name + " cooldown")

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

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(settings["authkey"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addTelegramCommandHandler("reactio", reactio)
    dp.addTelegramCommandHandler("kuva", kuva)
    dp.addTelegramCommandHandler("kiusua", insult)
    dp.addTelegramCommandHandler("new_insult", new_insult)


    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    update_queue = updater.start_polling(poll_interval=0.1, timeout=10)
    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.

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
