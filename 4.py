import requests

YOUR_ACCESS_TOKEN = 'pk.52663f975b8dec230bb40b8a11054d51'
def loc():
    url_1 = 'https://ramziv.com/ip'
    a = requests.get(url_1).text
    url = 'http://ipwhois.app/json/%s' % (a)
    response = requests.get(url)
    data = response.json()
    return data

url = 'https://maps.locationiq.com/v3/staticmap?key=%s&center=%s,%s&zoom=8&size=<width>x<height>&format=<format>&maptype=<MapType>&markers=icon:<icon>|<latitude>,<longitude>&markers=icon:<icon>|<latitude>,<longitude>' % (YOUR_ACCESS_TOKEN, loc()['latitude'], loc()['longitude'])
res = requests.get(url)
print(res.json())