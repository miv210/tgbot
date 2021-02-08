from library import config
import telebot
from telebot import types
from library.parser import pars1
from datetime import datetime, timedelta
from library.normly_parser import pars
from library.bd import read_bd

#Позваляет, не открывать doc фаил при каждом запросе, открывает раз в 5 мин для обновления time_table
def spam(text):
    global last_time
    global time_table
    time = datetime.now() - last_time
    seconds = time.seconds
    if seconds >=300:
        pars()
    last_time = datetime.now()
    time_table = read_bd(text)



bot = telebot.TeleBot(config.TOKEN)

last_time = datetime.now() - timedelta(minutes= 30)
time_table = ''


globalChat = {}

#При вводе комнды start создает кнопку
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    start = types.KeyboardButton('301Прг')
    sdad = types.KeyboardButton('101т')
    markup.add(start, sdad)

    bot.send_message(message.chat.id, '''Здесь вы можете получить замены учебных занятий, колледжа ВЭТК.
Комадны управления ботом:
/settings
/grups''', reply_markup= markup)

@bot.message_handler(commands=['settings'])
def ll(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("АвтоЗамены", callback_data='good')
    item2 = types.InlineKeyboardButton("АвтоЗамены", callback_data='bad')
    markup.add(item1,item2)


    bot.send_message(message.chat.id, 'Введите данные', reply_markup= markup)
@bot.message_handler(commands=['grups'])
def set_grups(message):
    bot.send_message(message.chat.id, 'Введите имя ваше группы в формате "301прг"')
    if message.text == message.text:
        marup = types.ReplyKeyboardMarkup(resize_keyboard= True)

        bot.send_message(message.chat.id, 'ваша группа', reply_markup=marup)
        group = types.KeyboardButton(message.text)
        marup.add(group)


@bot.message_handler(content_types=['text'])
def send_timetable(message):
    user_id = message.from_user.id
    if not user_id in globalChat:
        chat = {'sleep': 0}
        globalChat[user_id] = chat
    if globalChat[user_id]['sleep'] == 0:
        globalChat[user_id]['sleep'] = 1
        spam(message.text)
        global time_table
        bot.send_message(message.chat.id, time_table)
        globalChat[user_id]['sleep'] = 0
    else:
        bot.send_message(message.chat.id, 'Проверка расписания, ожидайте... ')
    print(globalChat)

@bot.callback_query_handler(func=lambda call: True)
def setting_board(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Working')
    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)