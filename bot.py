import telebot
import config
import requests
import vk
import random
from voice import say, recognize
import os
import time
import aneks

bot = telebot.TeleBot(config.token_telegram)

session = vk.Session(access_token=config.token_vk)
vk_api = vk.API(session)

@bot.message_handler(commands=['say'])
def say_m(message):
    file = open('ids.txt', 'r')
    a = file.readlines()
    anek = random.choice(a).strip()
    print(anek)
    bot.send_audio(message.chat.id, anek)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/say - рандомный (почти) анек голосом')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '/say - рандомный (почти) анек голосом')

@bot.message_handler(commands=['upload'])
def upload(message):
    if message.chat.id == config.admin_chat:
        try:
            n = int(message.text[8:])
        except:
            bot.send_message(message.chat.id, 'enter number')
            return
        anekdots = aneks.get(n)

        number = 0
        errors = 0
        start = 3844
        for i in range(start, len(anekdots)):
            try:
                token = config.token_yandex[number]
                errors = 0
                files = open('ids.txt', 'a')
                file = say(anekdots[i], token)
                audio = open(file, 'rb')
                msg = bot.send_audio(message.chat.id, audio)
                print(msg.audio.file_id, file=files)
                files.close()
                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
                os.remove(path)
                print(i, 'ready')
                time.sleep(1)
            except:
                bot.send_message(message.chat.id, 'SOME STRANGE ERROR' + str(i))
                errors += 1
                if errors >= 5:
                    bot.send_message(message.chat.id, 'OOOps, lots of errors, using the next token and sleeping 20 secs')
                    if number >= len(config.token_yandex):
                        bot.send_message(message.chat.id, 'no more tokens((')
                        files.close()
                        return
                    number += 1
                    time.sleep(20)
    else:
        bot.send_message(message.chat.id, 'You-re not admin')


if __name__ == '__main__':
    bot.polling(none_stop=True)