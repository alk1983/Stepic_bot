'''
Добрый день. Вот что сделал на данный момент. При переходе в состояние 'geophone' приходиться вызывать функцию сразу в
состоянии 'main' иначе до появления кнопок приходиться 2 раза нбирать команду '/geophone'.2 вопрос при переходе в состояние
'main' сделал удаление вызванных кнопок. Можно ли это сделать без печатания сообщения. Возможно об этом будет расказано в
уроке по кнопкам.3 вопрос сделал ввод координат в ручном режиме, но  есть идея сделать это через клик по карте, как это реализуется
на мобильных устройствах, когда у них отключена геолокация. Есть реализация в виде html файла javascript.Есть ли возможность
это прикрутить к телеграмм или какой-то другой способ? Сделал также способ определения координат
по ip адресу и прогноз погоды сюда пока не включал
'''

import telebot
from telebot import types
import requests
import json
from datetime import date, timedelta
import os



YOUR_ACCESS_TOKEN = 'pk.52663f975b8dec230bb40b8a11054d51'
def loc():
    url_1 = 'https://ramziv.com/ip'
    a = requests.get(url_1).text
    url = 'http://ipwhois.app/json/%s' % (a)
    response = requests.get(url)
    data = response.json()
    return data

def current_weather_temp (Lat, Lng):
    result = {} #создаем словарь result
    try:
        url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=af57c4e7dcdba3860df504a41c2c4070" % (
        float(Lat), float(Lng))  # отправляем запрос на апи
        response = requests.get(url, params={'lang': 'ru'})  # получаем ответ от апи
        data = response.json()  #
        result['middle_temp'] = (float(data['main']['temp']) - 273.15)
        if int(result['middle_temp']) > 0:
            result['middle_temp'] = '+' + str(int(result['middle_temp']))
        else:
            result['middle_temp'] = str(int(result['middle_temp']))
        result['name'] = data['name']
        for k in data['weather']:
            result['description'] = k['description']
        return result
    except Exception as e:
        result['middle_temp'] = 'нет ответа'
        result['name'] = 'нет ответа'
        result['description'] = 'нет овета'
        return result

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
states = {}
k = {}
MAIN_STATES = 'main'

def weater_temp(lat, lng):
    url = 'http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=af57c4e7dcdba3860df504a41c2c4070' % (float(lat), float(lng))
    result_2 = {}
    try:
        response = requests.get(url, params={'lang': 'ru'})
        data = response.json()
        for k in data['list']:
            result_2[k['dt_txt']] = {}
            result_2[k['dt_txt']]['temp'] = grad_cel(k['main']['temp'])
            for a in k['weather']:
                result_2[k['dt_txt']]['weather'] = a['description']
        return result_2
    except Exception as e:
        for k in range(0,3):
            result_2[date.today() + timedelta(days=k)] = {}
            result_2[date.today()+timedelta(days=k)]['temp'] = 'нет ответа'
            result_2[date.today()+timedelta(days=k)]['weather'] = 'нет ответа'

def geo_ip():
    data = {}
    try:
        url_1 = 'https://ramziv.com/ip'
        a = requests.get(url_1).text
        url = 'http://ipwhois.app/json/%s' % (a)
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        data['city'] = 'Не могу определить'
        data['latitude'] = 0
        data['longitude'] = 0
        return data

def grad_cel(temp):
    temp = (float(temp) - 273.15)
    if int(temp) > 0:
        temp = '+' + str(int(temp))
    else:
        temp = str(int(temp))
    return temp

@bot.message_handler(func= lambda message: True)
def dispatcher(message):
    user_id = message.from_user.id
    state = states.get(user_id, MAIN_STATES)

    if state == MAIN_STATES:
        weater(message)
    elif state == 'geo':
        input_geo(message)
        if states[message.from_user.id] != MAIN_STATES:
            send_message = 'Введите долготу и широту через пробел'
            bot.send_message(message.from_user.id, send_message)
    elif state == 'geophone':
        geophone(message)
    elif state == 'forecast':
        forecast(message)
    elif state == 'mape':
        mape(message)
    #print(state)

@bot.message_handler(func = lambda message: True)
def forecast(message):
    today = date.today()
    user_id = message.from_user.id
    region = current_weather_temp (k[user_id][-2], k[user_id][-1])['name']
    if message.text.lower() == 'сегодня':
        bot.send_message(user_id, 'Прогноз погоды в регионе {0}'.format(region))
        for key, val in weater_temp(k[user_id][-2], k[user_id][-1]).items():
            if str(today) in key:
                bot.send_message(user_id, '{0} температура {1} гр. С {2} '.format(key, val['temp'], val['weather']))
    elif message.text == '/cancel':
        states[user_id] = MAIN_STATES
        bot.send_message(user_id, 'Вы перешли в основное меню')
    elif message.text.lower() == 'завтра':
        bot.send_message(user_id, 'Прогноз погоды в регионе {0}'.format(region))
        for key, val in weater_temp(k[user_id][-2], k[user_id][-1]).items():
            if str(today+timedelta(days=1)) in key:
                bot.send_message(user_id, '{0} температура {1} гр. С {2} '.format(key, val['temp'], val['weather']))
    elif message.text.lower() == 'послезавтра':
        bot.send_message(user_id, 'Прогноз погоды в регионе {0}'.format(region))
        for key, val in weater_temp(k[user_id][-2], k[user_id][-1]).items():
            if str(today+timedelta(days=2)) in key:
                bot.send_message(user_id, '{0} температура {1} гр. С {2} '.format(key, val['temp'], val['weather']))

@bot.message_handler(func= lambda message: True)
def input_geo(message):
    user_id = message.from_user.id
    a = []
    if ' ' not in message.text:
        bot.reply_to(message, 'Неверный ввод')
    else:
        if message.text.split()[0].isalpha() or message.text.split()[1].isalpha():
            bot.reply_to(message, 'Неверный ввод')
        else:
            if message.from_user.id not in k.keys():
                k[user_id] = []
            a = message.text.split()
            k[user_id] += a
            bot.reply_to(message,'Верный ввод, возвращаетесь в основное меню')
            states[user_id] = MAIN_STATES

@bot.message_handler(func= lambda message: True)
def geophone(message):
    if message.text.lower() == 'ввести местоположение':
        states[message.from_user.id] = 'geo'
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Меню ручного ввода', reply_markup=a)
        send_message = 'Введите широту и долготу через пробел. Например Москва(Останкино) с.ш в.д "55.819543 37.611619" или Минск "53.8996 27.5585"'
        bot.send_message(message.from_user.id, send_message)
    elif message.text.lower() == 'местоположение по карте':
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Уточним ip адрес', reply_markup=a)
        markup = types.InlineKeyboardMarkup()
        url_1 = 'https://t.me/moypogoda_bot?start=H_1233423_aaac'
        markup.add(types.InlineKeyboardButton(text='Отправить ip адрес', url=url_1))
        bot.send_message(message.chat.id, 'Нажми кнопку внизу!', reply_markup=markup)
        states[message.from_user.id] = MAIN_STATES
    else:
        bot.send_message(message.from_user.id, 'Не понял')

@bot.callback_query_handler(func=lambda call: call)
def mape(call):
    user_id = call.from_user.id
    if call.data == 'ok':
        k[user_id].append(geo_ip()['latitude'])
        k[user_id].append(geo_ip()['longitude'])
        bot.send_message(call.from_user.id, 'Основное меню. Здесь можно узнать регион, погоду сейчас, прогноз погоды', reply_markup=None)
        states[call.from_user.id] = MAIN_STATES
    elif call.data == 'out':
        states[call.from_user.id] = 'geo'
        bot.send_message(call.from_user.id, 'Меню ручного ввода')
        send_message = 'Введите широту и долготу через пробел. Например Москва(Останкино) с.ш в.д "55.819543 37.611619" или Минск "53.8996 27.5585"'
        bot.send_message(call.from_user.id, send_message)
    else:
        bot.send_message(call.from_user.id,'Не понял')

@bot.message_handler(content_types=['location'])
def location_x (message):
    if message.from_user.id not in k.keys():
        k[message.from_user.id] = []
    #a = []
    #a.append(message.location.latitude)
    #a.append(message.location.longitude)
    k[message.from_user.id].append(message.location.latitude)
    k[message.from_user.id].append(message.location.longitude)
    bot.send_message(message.from_user.id,'Возвращаетесь в основное меню')
    if states[message.from_user.id] == 'geophone':
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Основное меню', reply_markup=a)
    states[message.from_user.id] = MAIN_STATES

@bot.message_handler(func= lambda message: True)
def weater(message):
    user_id = message.from_user.id
    #print(message.text)
    if message.text == '/start':
        bot.send_message(user_id,'Это погодный бот: он умеет подсказывать погоду в вашем регионе. Если Вы укажете свою '+
        'геолокацию, я покажу Вам: регион, погоду сейчас или прогноз погоды ')
        if user_id not in k.keys():
            k[user_id] = []
    elif '/start' in message.text:
        #print(message)
        if message.text.split()[1][0] == 'H':
            a = telebot.types.ReplyKeyboardRemove()
            bot.send_message(message.from_user.id, 'Меню ввода по карте', reply_markup=a)
            states[message.from_user.id] = 'mape'
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(text='Да', callback_data='ok'))
            url = 'https://maps.locationiq.com/v3/staticmap?key=%s&center=%s,%s&zoom=8&markers=icon:big-red-cut' % (
            YOUR_ACCESS_TOKEN, loc()['latitude'], loc()['longitude'])
            markup.add(types.InlineKeyboardButton(text='Нет уточнить по карте', url=url))
            markup.add(types.InlineKeyboardButton(text='Ввести значения', callback_data='out'))
            send_message = 'Ваше местоположение {0}'.format(geo_ip()['city'])
            bot.send_message(message.from_user.id, send_message)
            bot.send_message(message.chat.id, 'Нажми кнопку внизу!', reply_markup=markup)
    elif (message.text.lower() == 'погода сейчас' or message.text.lower() == 'прогноз погоды'or message.text.lower() == 'регион' ) and (len(k[user_id])<1):
        bot.send_message(user_id, 'Укажите Ваше местоположение командой /geophone')
    elif message.text.lower() == 'регион' and len(k[user_id])>1:
        bot.send_message(user_id, 'Регион '+'\n'+'с.ш: {0}'.format(k[user_id][-2]) +'\n'+'в.д {0}'.format(k[user_id][-1])+'\n'+
                     '{0}'.format(current_weather_temp (k[user_id][-2], k[user_id][-1])['name']))

    elif message.text.lower() == 'погода сейчас' and len(k[user_id])>1:
        bot.send_message(user_id, 'В регионе ' +current_weather_temp (k[user_id][-2], k[user_id][-1])['name']+
                     ' t: '+current_weather_temp (k[user_id][-2], k[user_id][-1])['middle_temp']+' гр. C, ' +
                         current_weather_temp (k[user_id][-2], k[user_id][-1])['description'])

    elif message.text == '/geophone':
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo_м_v = types.KeyboardButton(text="Ввести местоположение")
        buton_map = types.KeyboardButton(text="Местоположение по карте")
        button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo, button_geo_м_v,buton_map)
        bot.send_message(message.chat.id, "Поделись местоположением ", reply_markup=keyboard)
        states[user_id] = 'geophone'
    elif message.text.lower() == 'прогноз погоды' and len(k[user_id])>1:
        states[user_id] = 'forecast'
        bot.reply_to(message, 'Когда интересует погода. На сегодня, завтра, послезавтра')
    else:
        bot.reply_to(message, 'Я тебя не понял')


bot.polling()