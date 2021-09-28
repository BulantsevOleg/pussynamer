# -*- coding: utf-8 -*-
import telebot
from telebot import types
import random
from datetime import datetime, timezone
import requests
from urllib.request import urlopen

from textwrap import wrap

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from pussynamer_db import *
from pussynamer_text import *


# text = "Абубакар Хамим Аль-Багдади Рашид Эфенди"
# text = "Абубакар"


# ~~~~~~~~~~ BOT OPERATIONS ~~~~~~~~~~

TOKEN = '1969594443:AAEHHKGX1RaJIU9KLEcFnq5_DI5GFgJrlqQ'
bot = telebot.TeleBot(TOKEN)

note_status = "START"
pussy_name = ""

pussy_record = {}
button_new = types.KeyboardButton(text="/new_pussy")
button_show = types.KeyboardButton(text="/show_pussy")
button_save = types.KeyboardButton(text="/save_pussy")

# keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
# keyboard1.row('/create', '/get', '/end', '/update')

# ~~~~~~~~~~ MESSAGE HANDLERS ~~~~~~~~~~

@bot.message_handler(commands=['start'])
def start_message(message):
    global button_new
    keyboard_start = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    hello_text = "Привет! Этот бот поможет сохранить классные имена для ваших pussy😻\n\n/new_pussy – добавить новую киску в список\n/show_pussy – показать всех кисок из списка\n🐈‍⬛"
    keyboard_start.add(button_new)
    bot.send_message(message.chat.id, hello_text, reply_markup=keyboard_start)

@bot.message_handler(commands=["new_pussy"])
def new_pussy(message):
    global pussy_record
    global note_status
    id_user = message.from_user.id
    pussy_record["id_user"] = id_user
    rmv_keyboard = types.ReplyKeyboardRemove()
    print(pussy_record)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(message.chat.id, "Напиши имя своей pussy", reply_markup=rmv_keyboard)
    note_status = "IN PROGRESS"
    print(note_status)

@bot.message_handler(commands=["show_pussy"])
def show_pussy(message):
    global note_status
    keyboard_finish = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(message.chat.id, "Вот такие pussy уже есть в списке:", reply_markup=keyboard_finish)
    bot.send_message(message.chat.id, select())
    keyboard_finish.add(button_new)
    keyboard_finish.add(button_show)
    # note_status = "IN PROGRESS"

@bot.message_handler(content_types=['text'])
def add_pussy(message):
    global pussy_record
    global note_status
    global pussy_name
    global button_new
    # keyboard_finish = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    
    keyboard_approve = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    keyboard_approve.add(button_save)
    # keyboard_approve.add(button_new)

    if note_status == 'IN PROGRESS':
        pussy_name = message.text.title()
        pussy_record["pussy_name"] = pussy_name
        bot.send_message(message.chat.id, "Подтверди сохранение имени {} нажатием на кнопку /save_pussy".format(pussy_name),reply_markup=keyboard_approve)
        # note_status = 'ON APPROVE'
        bot.register_next_step_handler(message, save_pussy)

    # elif note_status == 'ON APPROVE':
    #     print("NAME", message.text.title())
    #     if message.text.title() != pussy_name:
    #         pussy_name = message.text.title()
    #         pussy_record["pussy_name"] = pussy_name
    #     bot.send_message(message.chat.id, "Подтверди сохранение имени {} нажатием на кнопку /save_pussy или просто напиши имя заново".format(pussy_name))
    #     bot.register_next_step_handler(message, save_pussy)


@bot.message_handler(commands=["save_pussy"])
def save_pussy(message):
    global pussy_record
    global pussy_name
    global note_status
    print(pussy_name)

    keyboard_finish = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    
    keyboard_finish.add(button_new)
    keyboard_finish.add(button_show)
    # отправить в БД
    created_on_field = datetime.fromtimestamp(message.date).strftime('%Y-%m-%dT%H:%M:%S')
    print(created_on_field)
    user_field = pussy_record["id_user"]
    pussyname_field = pussy_record["pussy_name"]

    # INSERT TO DB USER NOTES
    insert(user_field, created_on_field, pussyname_field)
    kitty = "👁    👁\n>   ⚮   <\n     👅"
    bot.send_message(message.chat.id, "Твоя pussy добавлена в список имен!\n\n{}\n".format(kitty), reply_markup=keyboard_finish)
    # Place name of the pussy on the image
    pussy_image = caption_img(pussy_name)
    bot.send_photo(message.chat.id, photo=pussy_image)
    # bot.register_next_step_handler(message, save_note)
    # pussy_record[]
    print(pussy_record)
    # bot.register_next_step_handler(message, save_note)
    
    note_status = "START"
    
    # elif note_status == "FINISH":
    #     bot.send_message(message.chat.id, "Ты только что добавил новую киску. Теперь можешь посмотреть список имен или добавить новое.")
    #     keyboard_finish.add(button_new)
    #     keyboard_finish.add(button_show)
    # else:
    #     bot.send_message(message.chat.id, "Error: бот не понял сообщение. Лучше вернись в главное меню")
    #     keyboard_finish.add(button_new)
    #     keyboard_finish.add(button_show)
    
    
    
bot.polling(none_stop=True, interval=0)