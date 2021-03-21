import requests
import json
import re
from bs4 import BeautifulSoup
def decod_YP(text):
    a = text.split('_')
    YP = ''
    count = 0
    for i in range(0,len(a[2])):
        if a[2][i] == 'a':
            YP += a[1][count:count+3]
            count += 3
            print (count)
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

print(decod_YP('H_17812131134_aaba'))
url_1 = 'https://ramziv.com/ip'
a = requests.get(url_1).text
url = 'http://ipwhois.app/json/%s'%(a)
response = requests.get(url)
data = response.json()
print(response.json())
class RockBand:
    genre = "rock"
    members = []
    famous_songs = {}
    def n_members(self):
        return len(RockBand.members)
    def add_members(self,k):
        RockBand.members.append(k)
    def add_song(self,k,v):
        self.famous_songs[k] = v
    def  most_popular_song(self):
        pop = 0
        for k,v in self.famous_songs.items():
            if v > pop:
                pop = v
                son = k
        return son


band = RockBand()
band.add_members('Jon')
band.add_members('Jim')
band.add_members('Erl')
band.add_members('Alex')
band.add_song("'Rock'n'roll",10)
band.add_song("Roc",6)
band.add_song("Noic",5)
print(band.n_members())
print(band.most_popular_song())


#url1 = input()
#url2 = input()
url1 = 'https://stepic.org/media/attachments/lesson/24472/sample0.html'
url2 = 'https://stepic.org/media/attachments/lesson/24472/sample2.html'
'''
def url1(url):
    a = []
    res_1 = requests.get(url)
    soup = BeautifulSoup(res_1.text, 'html.parser')
    for link in soup.find_all('a'):
        a.append(link.get('href'))
    return a

#print (a)
yn = 'No'
for k in url1(url1):
    for l in url1(k):
        if l == url2:
            yn = 'Yes'
            break
print (yn)
'''
def url (url):
    patern = r"<a href=\"(.*)\">"
    res_1 = requests.get(url)
    link = re.findall(patern, res_1.text)
    return link
yn = 'No'
for k in url (url1):
    for l in url (k):
        if l == url2:
            yn = 'Yes'
            break
print (yn)