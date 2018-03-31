import telebot
import config
import vk
import random

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



if __name__ == '__main__':
    bot.polling(none_stop=True)