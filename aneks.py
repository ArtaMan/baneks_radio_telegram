import vk
import config
from voice import say


def get_all():
    session = vk.Session(access_token=config.token_vk)
    vk_api = vk.API(session)

    count = vk_api.wall.get(domain="baneks", offset=0, count=1)[0]

    aneks = []
    fout = open('baneks.txt', 'w')

    for i in range(count // 100):
        record = vk_api.wall.get(domain="baneks", offset=i, count=100)
        for j in range(1, len(record) - 1):
            txt = record[j]['text'].replace('<br>', ' ')
            aneks.append(txt)
        print(i, 'ready')
    print(aneks, file=fout)
    print('done')

def get_ten():
    session = vk.Session(access_token=config.token_vk)
    vk_api = vk.API(session)

    aneks = []

    record = vk_api.wall.get(domain="baneks", offset=0, count=10)
    for j in range(1, len(record) - 1):
        txt = record[j]['text'].replace('<br>', ' ')
        aneks.append(txt)

    return aneks

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

def upload():
    # with open('baneks.txt', 'r') as f:
    #     a = f.readline()
    #     print(a)

    aneks = get_ten()
    for i in range(len(aneks)):
        file = say(aneks[i])
        audio = open(file, 'rb')