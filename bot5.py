'''
Добрый день.
'''

import telebot
from telebot import types
import requests
import json
from datetime import date, timedelta
import os
import redis

redis_url = os.environ.get('REDIS_URL')
#dict_ob = {
#'k1190926674': '{"1190926674": [54.0, 67.0, "52.4411761", "30.9878461"]}', 'state1190926674': 'main',
 #'My_IP1190926674': '{"1190926674": "178.121.31.134"}'}
try:
    if redis_url is None:
        dict_ob = json.load(open('data.json', 'r', encoding= 'utf-8'))
    else:
        redis_ob = redis.from_url(redis_url)
        dict_ob = json.loads(redis_ob.get('data'))
        if dict_ob is None:
            dict_ob = {}
except Exception as e:
    dict_ob = {}

def save(key, value):
    if redis_url:
        redis_ob = redis.from_url(redis_url)
        dict_ob[key] = value
        redis_ob.set('data', json.dumps(dict_ob))
    else:
        dict_ob[key] = value
        json.dump(dict_ob, open('data.json', 'w', encoding='utf-8'))


def load_(key):
    return dict_ob.get(key)

def init_k(user_id):
    if load_('k{0}'.format(user_id)) is None:
        k[user_id] = []
    else:
        k[user_id] = json.loads(load_('k{0}'.format(user_id)))



YOUR_ACCESS_TOKEN = 'pk.52663f975b8dec230bb40b8a11054d51'
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
states = {}
k = {}
My_IP = {}
MAIN_STATES = 'main'

@bot.message_handler(func= lambda message: True)
def dispatcher(message):
    user_id = str(message.from_user.id)
    state = load_('state{0}'.format(user_id))
    if state is None:
        state = states.get(user_id, MAIN_STATES)
        save('state{0}'.format(user_id), state)
    #k = json.loads(load_('k{0}'.format(user_id)))
    #My_IP = json.loads(load_('My_IP{0}'.format(user_id)))
    if state == MAIN_STATES:
        weater(message)

    elif state == 'geo':
        input_geo(message)

    elif state == 'geophone':
        geophone(message)
    elif state == 'forecast':
        forecast(message)
    elif state == 'mape':
        mape(message)
    #print(state)




def buton_in_forecast(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_today = types.KeyboardButton(text="Сегодня")
    button_tom = types.KeyboardButton(text="Завтра")
    button_for = types.KeyboardButton(text="Послезавтра")
    keyboard.add(button_today, button_tom, button_for)
    bot.send_message(message.from_user.id, "Нажми кнопку или напиши сообщение ", reply_markup=keyboard)


def buton_in_main(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_today = types.KeyboardButton(text="Погода сейчас")
    buton_reg = types.KeyboardButton(text="Выбранный район")
    button_for = types.KeyboardButton(text="Прогноз погоды")
    keyboard.add(button_today, button_for, buton_reg)
    bot.send_message(message.from_user.id, "Нажми кнопку или напиши сообщение ", reply_markup=keyboard)


def buton_geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo_м_v = types.KeyboardButton(text="Ввести местоположение")
    buton_map = types.KeyboardButton(text="Местоположение по карте")
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo, button_geo_м_v, buton_map)
    bot.send_message(message.chat.id, "Поделись местоположением ", reply_markup=keyboard)

def loc_host():
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


def decod_Cord(text):
    try:
        a = []
        b = text.split('_')
        a.append(float(b[1])+ float(int(b[2])/(10**len(b[2]))))
        a.append(float(b[3])+ float(int(b[4])/(10**len(b[4]))))
        return a
    except Exception as e:
        a.append(53.45)
        a.append(45.24)
        return a

def decod_YP(text):
    a = text.split('_')
    YP = ''
    count = 0
    for i in range(0,len(a[2])):
        if a[2][i] == 'a':
            YP += a[1][count:count+3]
            count += 3
        elif a[2][i] == 'b':
            YP += a[1][count:count + 2]
            count += 2
        elif a[2][i] == 'c':
            YP += a[1][count]
            count += 1
        if i == 3:
            break
        YP += '.'
    return YP


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
def geo_IP(YP):
    try:
        url = 'http://ipwhois.app/json/%s' % (YP)
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


@bot.message_handler(func = lambda message: True)
def forecast(message):
    today = date.today()
    user_id = str(message.from_user.id)
    region = current_weather_temp (k[user_id][-2], k[user_id][-1])['name']
    if message.text.lower() == 'сегодня':
        bot.send_message(user_id, 'Прогноз погоды в регионе {0}'.format(region))
        for key, val in weater_temp(k[user_id][-2], k[user_id][-1]).items():
            if str(today) in key:
                bot.send_message(user_id, '{0} t {1} гр. С, {2} '.format(key, val['temp'], val['weather']))
    elif message.text == '/cancel':
        states[user_id] = MAIN_STATES
        save('state{0}'.format(user_id), states[user_id])
        bot.send_message(user_id, 'Вы перешли в основное меню')
        buton_in_main(message)
    elif message.text.lower() == 'завтра':
        bot.send_message(user_id, 'Прогноз погоды в регионе {0}'.format(region))
        for key, val in weater_temp(k[user_id][-2], k[user_id][-1]).items():
            if str(today+timedelta(days=1)) in key:
                bot.send_message(user_id, '{0} t {1} гр. С, {2} '.format(key, val['temp'], val['weather']))
    elif message.text.lower() == 'послезавтра':
        bot.send_message(user_id, 'Прогноз погоды в регионе {0}'.format(region))
        for key, val in weater_temp(k[user_id][-2], k[user_id][-1]).items():
            if str(today+timedelta(days=2)) in key:
                bot.send_message(user_id, '{0} t {1} гр. С, {2} '.format(key, val['temp'], val['weather']))

@bot.message_handler(func= lambda message: True)
def input_geo(message):
    user_id = str(message.from_user.id)
    a = []
    if ' ' not in message.text:
        bot.reply_to(message, 'Неверный ввод, повторите ввод. Цифры вводите через пробел')
    else:
        init_k(user_id)
        a = message.text.split()
        try:
            float(a[0])
            float(a[1])
            if float(a[0]) >= 90 or float(a[0]) <= -90 or float(a[1]) > 180 or float(a[1]) < -180:
                bot.reply_to(message, 'Неверный ввод, первая координата от - 90 до +90, вторая от  -180 до +180')
            else:
                k[user_id].append(float(a[0]))
                k[user_id].append(float(a[1]))
                save('k{0}'.format(user_id), json.dumps(k[user_id]))
                bot.reply_to(message, 'Верный ввод, возвращаетесь в меню ввода по карте')
                states[user_id] = 'mape'
                save('state{0}'.format(user_id), states[user_id])
                func_mape(message.from_user.id, k[user_id][-2], k[user_id][-1])

        except:
            bot.send_message(user_id,
            'Неверный ввод, повторите ввод. Вводите только цифры, для отделения дробной части используйте точку')

            #print(a)

@bot.message_handler(func= lambda message: True)
def geophone(message):

    user_id = str(message.from_user.id)
    init_k(user_id)
    if message.text.lower() == 'ввести местоположение':
        states[user_id] = 'geo'
        save('state{0}'.format(user_id), states[user_id])
        #print (states[user_id])
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Меню ручного ввода', reply_markup=a)
        send_message = 'Введите широту и долготу через пробел. Например Москва(Останкино) с.ш в.д "55.819543 37.611619" или Минск "53.8996 27.5585"'
        bot.send_message(message.from_user.id, send_message)
    elif message.text.lower() == 'местоположение по карте':
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Уточним ip адрес для инициализации карты или введи'+
             ' ориентировочные координаты', reply_markup=a)
        markup = types.InlineKeyboardMarkup()
        url_1 = 'https://zerkalo1983.herokuapp.com'
        markup.add(types.InlineKeyboardButton(text='Отправить ip адрес', url=url_1))
        if len(k[user_id]) >= 2:
            markup.add(types.InlineKeyboardButton(text='Посмотреть введённые ранее значения', callback_data='init'))

        markup.add(types.InlineKeyboardButton(text='Ввести значения', callback_data='out'))
        bot.send_message(message.chat.id, 'Нажми кнопку внизу!', reply_markup=markup)
        states[user_id] = 'mape'
        save('state{0}'.format(user_id), states[user_id])
    else:
        bot.send_message(message.from_user.id, 'Не понял')
        buton_geo(message)

@bot.callback_query_handler(func=lambda call: call)
def mape(call):
    user_id = str(call.from_user.id)
    #print(call)
    if isinstance(call, telebot.types.CallbackQuery):
        if call.data == 'ok':
            #save('k_keys', json.dumps(k))
            #k[user_id].append(geo_ip()['latitude'])
            #k[user_id].append(geo_ip()['longitude'])
            bot.send_message(call.from_user.id,
            'Основное меню. Здесь можно узнать регион, погоду сейчас, прогноз погоды',
            reply_markup=None)
            states[user_id] = MAIN_STATES
            save('state{0}'.format(user_id), states[user_id])
            buton_in_main(call)
        elif call.data == 'out':
            states[str(call.from_user.id)] = 'geo'
            save('state{0}'.format(user_id), states[user_id])
            bot.send_message(call.from_user.id, 'Меню ручного ввода')
            send_message = 'Введите широту и долготу через пробел. Например Москва(Останкино) с.ш в.д "55.819543 37.611619" или Минск "53.8996 27.5585"'
            bot.send_message(call.from_user.id, send_message)
        elif call.data == 'init':
            func_mape(call.from_user.id, k[user_id][-2], k[user_id][-1])
    else:
        if '/start' in call.text and len(call.text.split()) > 1:

            if call.text.split()[1][0] == 'H':
                decod_YP(call.text.split()[1])
                My_IP[str(call.from_user.id)] = decod_YP(call.text.split()[1])
                geo_IP(My_IP[str(call.from_user.id)])
                save('My_IP{0}'.format(user_id), json.dumps(My_IP))
                k[user_id].append(geo_IP(My_IP[user_id])['latitude'])
                k[user_id].append(geo_IP(My_IP[user_id])['longitude'])
                save('k{0}'.format(user_id), json.dumps(k[user_id]))

                func_mape(call.from_user.id, k[user_id][-2], k[user_id][-1])
            elif call.text.split()[1][0] == 'L':

                k[user_id] += decod_Cord(call.text.split()[1])
                save('k{0}'.format(user_id), json.dumps(k[user_id]))
                func_mape(call.from_user.id, k[user_id][-2], k[user_id][-1])

        else:
            bot.send_message(call.from_user.id,'Не понял')

def func_mape(call_from_user_id, lat, lon):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(call_from_user_id, 'Меню ввода по карте', reply_markup=a)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Да', callback_data='ok'))
    url = 'https://maps1983.herokuapp.com/?lan=%s&lon=%s'% (lat, lon)
    markup.add(types.InlineKeyboardButton(text='Нет уточнить по карте', url=url))
    markup.add(types.InlineKeyboardButton(text='Ввести значения', callback_data='out'))
    send_message = 'Ваше местоположение {0}'.format(current_weather_temp(lat, lon)['name'])
    bot.send_message(call_from_user_id, send_message)
    bot.send_message(call_from_user_id, 'Нажми кнопку внизу!', reply_markup=markup)

@bot.message_handler(content_types=['location'])
def location_x (message):
    user_id = str(message.from_user.id)
    init_k(user_id)
    #a = []
    #a.append(message.location.latitude)
    #a.append(message.location.longitude)
    k[user_id].append(message.location.latitude)
    k[user_id].append(message.location.longitude)
    save('k{0}'.format(user_id), json.dumps(k[user_id]))

    bot.send_message(message.from_user.id,'Возвращаетесь в основное меню')
    if states[user_id] == 'geophone':
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Основное меню', reply_markup=a)
        buton_in_main(message)
    states[message.from_user.id] = MAIN_STATES
    save('state{0}'.format(message.from_user.id), states[message.from_user.id])




@bot.message_handler(func= lambda message: True)
def weater(message):
    user_id = str(message.from_user.id)
    init_k(user_id)
    #print(k, '123')
        #print(1)

    if message.text == '/start':
        bot.send_message(user_id,'Это погодный бот: он умеет подсказывать погоду в вашем регионе. Если Вы укажете свою '+
        'геолокацию, я покажу Вам: регион, погоду сейчас или прогноз погоды ')
        buton_in_main(message)
    elif (message.text.lower() == 'погода сейчас' or message.text.lower() == 'прогноз погоды'or message.text.lower() == 'выбранный район' ) and (len(k[user_id])<1):
        bot.send_message(user_id, 'Укажите Ваше местоположение командой /geophone')
    elif message.text.lower() == 'выбранный район' and len(k[user_id]) > 1:
        bot.send_message(user_id, 'Регион '+'\n'+'с.ш: {0}'.format(k[user_id][-2]) +'\n'+'в.д {0}'.format(k[user_id][-1])+'\n'+
                     '{0}. '.format(current_weather_temp (k[user_id][-2], k[user_id][-1])['name'])+'для выбора другого района нажми /geophone')

    elif message.text.lower() == 'погода сейчас' and len(k[user_id])>1:
        bot.send_message(user_id, 'В регионе ' +current_weather_temp (k[user_id][-2], k[user_id][-1])['name']+
                     ' t: '+current_weather_temp (k[user_id][-2], k[user_id][-1])['middle_temp']+' гр. C, ' +
                         current_weather_temp (k[user_id][-2], k[user_id][-1])['description'])

    elif message.text == '/geophone':
        buton_geo(message)
        states[user_id] = 'geophone'
        save('state{0}'.format(user_id), states[user_id])
    elif message.text == 'host':
        a = telebot.types.ReplyKeyboardRemove()
        url = 'https://maps.locationiq.com/v3/staticmap?key=%s&center=%s,%s&zoom=8&markers=icon:big-red-cut' % (
            YOUR_ACCESS_TOKEN, loc_host()['latitude'], loc_host()['longitude'])
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text='Сервер на карте', url=url))
        bot.send_message(message.chat.id, 'Нажми кнопку внизу, чтобы посмотреть где сервер', reply_markup=markup)

    elif message.text.lower() == 'прогноз погоды' and len(k[user_id])>1:
        states[user_id] = 'forecast'
        save('state{0}'.format(user_id), states[user_id])
        bot.reply_to(message, 'Когда интересует погода. На сегодня, завтра, послезавтра. '+
        'Для перехода в основное меню введите /cancel')
        buton_in_forecast(message)
    elif '/start' in message.text and len(message.text.split()) > 1:
        bot.send_message(message.chat.id, 'Перейдите в меню выбора местоположения по карте командой /geophone')
    else:
        bot.reply_to(message, 'Я тебя не понял')
        buton_in_main(message)



bot.polling()
print('gtht')



