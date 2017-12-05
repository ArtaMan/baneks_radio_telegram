import telebot
import config
import requests
import vk
import config2
from random import choice
from voice import say, recognize

bot = telebot.TeleBot(config.token)

session = vk.Session(access_token=config2.token)
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
        audio = open(say(random_record['text']), 'rb')
        bot.send_audio(message.chat.id, audio)
        print('done')
    except:
        pass

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '/say - рандомный (почти) анек голосом')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '/say - рандомный (почти) анек голосом')


if __name__ == '__main__':
    bot.polling(none_stop=True)