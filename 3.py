import requests

with open('D:/input.txt') as inf:
    for k in inf:
        k = k.strip()
        url = 'http://numbersapi.com/%s/math?json=true'%(k)
        res = requests.get(url)
        data = res.json()
        if data['found'] == True:
            print('Interesting')
        else:
            print('Boring')

