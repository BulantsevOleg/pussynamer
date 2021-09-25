# -*- coding: utf-8 -*-
import telebot
from telebot import types
import random
from datetime import datetime, timezone
# import psycopg2
from pussynamer_db import *


# ~~~~~~~~~~ BOT OPERATIONS ~~~~~~~~~~

TOKEN = '1969594443:AAEHHKGX1RaJIU9KLEcFnq5_DI5GFgJrlqQ'
bot = telebot.TeleBot(TOKEN)

note_status = "START"
pussy_name = ""

pussy_record = {}
button_new = types.KeyboardButton(text="/new_pussy")
button_show = types.KeyboardButton(text="/show_pussy")


# keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
# keyboard1.row('/create', '/get', '/end', '/update')

# ~~~~~~~~~~ MESSAGE HANDLERS ~~~~~~~~~~

@bot.message_handler(commands=['start'])
def start_message(message):
    global button_new
    keyboard_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    hello_text = "Привет! Этот бот поможет сохранить классные имена для ваших pussy😻\n\n/new_pussy – добавить новую киску в список\n/show_pussy – показать всех кисок из списка\n🐈‍⬛"
    button_new
    keyboard_start.add(button_new)
    bot.send_message(message.chat.id, hello_text, reply_markup=keyboard_start)

@bot.message_handler(commands=["new_pussy"])
def new_pussy(message):
    global pussy_record
    global note_status
    id_user = message.from_user.id
    pussy_record["id_user"] = id_user
    print(pussy_record)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    # button_geo = types.KeyboardButton(text="Отправить местоположение 📍", request_location=True)
    # keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Напиши имя своей pussy", reply_markup=keyboard)
    note_status = "WAITING"
    print(note_status)

@bot.message_handler(commands=["show_pussy"])
def show_pussy(message):
    bot.send_message(message.chat.id, "Вот такие pussy уже есть в списке:")
    bot.send_message(message.chat.id, select())


@bot.message_handler(content_types=['text'])
def add_note(message):
    global pussy_record
    # pussy_record = {}
    # print("!!!!!!CHECKING",lat, lon)
    global pussy_name
    # print(note_status)
    if note_status == 'WAITING':
        keyboard_finish = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        # new_name = types.KeyboardButton(text="/start")
        keyboard_finish.add(button_new)
        # select_button = types.KeyboardButton(text="/показать весь список pussy")
        keyboard_finish.add(button_show)
        pussy_name = message.text
        pussy_record["pussy_name"] = pussy_name
        # отправить в БД
        created_on_field = datetime.fromtimestamp(message.date).strftime('%Y-%m-%dT%H:%M:%S')
        print(created_on_field)
        user_field = pussy_record["id_user"]
        pussyname_field = pussy_record["pussy_name"]

        # INSERT TO DB USER NOTES
        insert(user_field, created_on_field, pussyname_field)
        bot.send_message(message.chat.id, "Congratulations!\nВаша pussy добавлена в список имен!", reply_markup=keyboard_finish)
        # bot.register_next_step_handler(message, save_note)
        # pussy_record[]
        print(pussy_record)
        # bot.register_next_step_handler(message, save_note)
    else:
        bot.send_message(message.chat.id, "ОШИБКА: БОТ НЕ ЖДЕТ ТЕКСТ")

# @bot.message_handler(commands=["save"])
# def save_note(message):
#     global pussy_record
#     # created_on_field = str(datetime.fromtimestamp(message.date))
#     created_on_field = datetime.fromtimestamp(message.date).strftime('%Y-%m-%dT%H:%M:%S')
#     print(created_on_field)
#     user_field = pussy_record["id_user"]
#     pussyname_field = pussy_record["pussy_name"]

#     # INSERT TO DB USER NOTES
#     insert(user_field, created_on_field, pussyname_field)
    
bot.polling(none_stop=True, interval=0)