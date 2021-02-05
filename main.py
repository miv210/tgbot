from library import config
import telebot
from telebot import types
from library.parser import pars1
from datetime import datetime, timedelta
from library.normly_parser import pars

#Позваляет, не открывать doc фаил при каждом запросе, открывает раз в 5 мин для обновления time_table
def spam(text):
    global last_time
    global time_table
    time = datetime.now() - last_time
    seconds = time.seconds
    if seconds >=300:
        last_time = datetime.now()
        time_table = pars(text)



bot = telebot.TeleBot(config.TOKEN)

last_time = datetime.now() - timedelta(minutes= 30)
time_table = ''


globalChat = {}

#При вводе комнды start создает кнопку
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    start = types.KeyboardButton('301Прг')
    markup.add(start)

    bot.send_message(message.chat.id, "Здесь вы можете получить расписание учебных занятий, колледжа ВЭТК", reply_markup= markup)

@bot.message_handler(content_types=['text'])
def send_timetable(message):
    user_id = message.from_user.id
    if message.text == '301Прг':
        if not user_id in globalChat:
            chat = {'sleep': 0}
            globalChat[user_id] = chat
        if globalChat[user_id]['sleep'] == 0:
            # исполнение парсера
            globalChat[user_id]['sleep'] = 1
            spam(message.text)
            global time_table
            bot.send_message(message.chat.id, time_table)
            globalChat[user_id]['sleep'] = 0
        else:
            bot.send_message(message.chat.id, 'Проверка расписания, ожидайте... ')
    print(globalChat)

bot.polling(none_stop=True)