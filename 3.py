import requests
import redis
import os
import json


redis_url = os.environ.get('REDIS_URL')
dict_ob = {}
def load_(key):
    if redis_url:
        redis_ob = redis.from_url(redis_url)
        return redis_ob.get(key)
    else:
        return dict_ob.get(key)

print(load_(123))

#save('k{0}'.format(user_id), json.dumps(k))
#save('k', json.dumps(k))

dict_ob = json.load(open('data.json', 'r', encoding= 'utf-8'))

print(json.loads(dict_ob["k1190926674"])[0])