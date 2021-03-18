import requests
from datetime import date, timedelta
import json
API_KEY = 'af57c4e7dcdba3860df504a41c2c4070'
def current_weather_temp (Lat, Lng):
    result = {} #создаем словарь result
    url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&appid=af57c4e7dcdba3860df504a41c2c4070" %(float(Lat), float(Lng)) #отправляем запрос на апи
    response = requests.get(url,params={'lang':'ru'}) #получаем ответ от апи
    data = response.json()#
    result['middle_temp'] = (float(data['main']['temp'])-273.15)
    if int(result['middle_temp']) > 0:
        result['middle_temp'] = '+'+str(int(result['middle_temp']))
    else:
        result['middle_temp'] = str(int(result['middle_temp']))
    result['name'] = data ['name']
    for k in data ['weather']:
        result['description'] = k['description']
    return result

def grad_cel(temp):
    temp = (float(temp) - 273.15)
    if int(temp) > 0:
        temp = '+' + str(int(temp))
    else:
        temp = str(int(temp))
    return temp

def weater_temp(lat, lng):
    url = 'http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=af57c4e7dcdba3860df504a41c2c4070' % (float(lat), float(lng))
    result_2 = {}
    response = requests.get(url, params={'lang': 'ru'})
    data = response.json()
    for k in data['list']:
        result_2[k['dt_txt']] = {}
        result_2[k['dt_txt']]['temp'] = grad_cel(k['main']['temp'])
        for a in k['weather']:
            result_2[k['dt_txt']]['weather'] = a['description']
    return result_2

Kiev_lat = 50.450026 #широта киева
Kiev_lng = 30.524003 #долгота киева
M_lat = 52.025712
M_Lng = 29.206491
today = date.today()
print (current_weather_temp(M_lat, M_Lng))
print(current_weather_temp(M_lat, M_Lng)['name'])
print(weater_temp(M_lat,M_Lng))
print(today)
for key, val in weater_temp(M_lat,M_Lng).items():
    if str(today) in key:
        print('{0} температура {1} гр. С {2} '.format(key, val['temp'], val['weather']))
result_3 = {}
for k in range(0,3):
     result_3[str(date.today()+timedelta(days=k))] = {}
     result_3[str(date.today()+timedelta(days=k))]['temp'] = 'нет ответа'
     result_3[str(date.today()+timedelta(days=k))]['weather'] = 'нет ответа'
print (result_3)