import vk
import config
from voice import say

def get(n):
    session = vk.Session(access_token=config.token_vk)
    vk_api = vk.API(session)

    aneks = []

    for i in range(n // 100):
        record = vk_api.wall.get(domain="baneks", offset=i, count=100)
        for j in range(1, len(record)):
            txt = record[j]['text'].replace('<br>', ' ')
            aneks.append(txt)
        print(i, 'done')

    print('doing the last', n % 100)
    record = vk_api.wall.get(domain="baneks", offset=0, count = n % 100)
    for j in range(1, len(record)):
        txt = record[j]['text'].replace('<br>', ' ')
        aneks.append(txt)
    print('all done')

    return aneks
