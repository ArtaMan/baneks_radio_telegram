import telebot
import config
import requests
import vk
from random import choice
from voice import say, recognize
import os
import time
import aneks

bot = telebot.TeleBot(config.token_telegram)

session = vk.Session(access_token=config.token_vk)
vk_api = vk.API(session)

@bot.message_handler(commands=['say'])
def say_m(message):
    themes = ['петрович', 'вовочка', 'мужик', 'петька', 'a', 'девушка', '']
    records = vk_api.wall.search(domain='baneks', query=choice(themes), owners_only=1, v=5.68, count=100)
    # for i in range(10):
    try:
        print('sending')
        bot.send_message(message.chat.id, 'sending')
        random_record = choice(records['items'])
        file = say(random_record['text'])
        audio = open(file, 'rb')
        bot.send_audio(message.chat.id, audio)
        print('done')
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
        os.remove(path)
    except:
        pass

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/say - рандомный (почти) анек голосом')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '/say - рандомный (почти) анек голосом')

@bot.message_handler(commands=['upload'])
def upload(message):
    try:
        n = int(message.text[8:])
    except:
        bot.send_message(message.chat.id, 'enter number')
        return
    anekdots = aneks.get(n)

    for i in range(len(anekdots)):
        try:
            files = open('ids.txt', 'a')
            file = say(anekdots[i])
            audio = open(file, 'rb')
            msg = bot.send_audio(message.chat.id, audio)
            print(msg.audio.file_id, file=files)
            files.close()
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
            os.remove(path)
            time.sleep(1)
        except:
            print('SOME STRANGE ERROR', i)

if __name__ == '__main__':
    bot.polling(none_stop=True)