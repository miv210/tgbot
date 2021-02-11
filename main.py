from library import config
import telebot
from telebot import types

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
        last_time = datetime.now()
        pars()
    time_table = read_bd(text)

def global_chat_save(user_id, group = 'Не указана группа'):
    if not user_id in globalChat:
        chat = {'sleep': 0, 'group': group}
        globalChat[user_id] = chat
    globalChat[user_id]['group'] = group

bot = telebot.TeleBot(config.TOKEN)

last_time = datetime.now() - timedelta(minutes= 30)
time_table = ''


globalChat = {}

#При вводе комнды start создает кнопку
@bot.message_handler(commands=['start'], content_types=['text'])
def welcome(message):
    marup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    save_button = types.KeyboardButton('Получить расписание')
    change_group = types.KeyboardButton('Изменить имя группы')
    marup.add(save_button, change_group)
    main = bot.send_message(message.chat.id, '''Чтобы узнать расписание введите название группы в формате "301прг" ''', reply_markup= marup)
    if message.text == 'Получить расписание':

        bot.register_next_step_handler(main, buttons)


def buttons(message):
    markup = types.InlineKeyboardMarkup()
    save = types.InlineKeyboardButton('Сохранить', callback_data='save')
    change = types.InlineKeyboardButton('Изменить', callback_data='change')
    markup.add(save, change)


    if message.text:
        global_chat_save(message.from_user.id, message.text)
        bot.send_message(message.chat.id, 'Ваша группа {0} ?'.format(message.text), reply_markup= markup)

@bot.message_handler(content_types=['text'])
def send_timetable(message):

    user_id = message.from_user.id
    global_chat_save(user_id)



    if globalChat[user_id]['sleep'] == 0:
        globalChat[user_id]['sleep'] = 1
        spam(globalChat[user_id]['group'])
        global time_table
        bot.send_message(message.chat.id, time_table)
        globalChat[user_id]['sleep'] = 0
    else:
        bot.send_message(message.chat.id, 'Проверка расписания, ожидайте... ')
    print(globalChat[user_id])


@bot.callback_query_handler(func=lambda call:True)
def call_back(call):
    try:
        if call.message:
            if call.data== 'save':
                save = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Сохраненно')
                bot.register_next_step_handler(save, send_timetable)

            elif call.data == 'change':
                change = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Внесите зменения')
                bot.register_next_step_handler(change, buttons)

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)