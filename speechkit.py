import xml.etree.ElementTree as XmlElementTree
import httplib2
import urllib.request
import urllib.parse
import uuid
import time
import ssl
import config

ssl._create_default_https_context = ssl._create_unverified_context

YANDEX_ASR_HOST = 'asr.yandex.net'
YANDEX_ASR_PATH = '/asr_xml'
CHUNK_SIZE = 1024 ** 2
RATE = 16000
PCM_CHUNK = 1024
THRESHOLD_AFTER_ACTIVATION = 200
THRESHOLD = 200

launch_time = time.time()


def log(s):
    elapsed = time.time() - launch_time
    print(("[%02d:%02d] " % (int(elapsed // 60), int(elapsed % 60))) + str(s))


def read_chunks(chunk_size, byte_data):
    while True:
        chunk = byte_data[:chunk_size]
        byte_data = byte_data[chunk_size:]

        yield chunk

        if not byte_data:
            break


def record_to_text(data, key, request_id=uuid.uuid4().hex, topic='notes', lang='ru-RU'):
    log("Считывание блока байтов")
    chunks = read_chunks(CHUNK_SIZE, data)

    log("Установление соединения")
    connection = httplib2.HTTPConnectionWithTimeout(YANDEX_ASR_HOST)

    url = YANDEX_ASR_PATH + '?uuid=%s&key=%s&topic=%s&lang=%s' % (
        request_id,
        key,
        topic,
        lang
    )

    log("Запрос к Yandex API")
    connection.connect()
    connection.putrequest('POST', url)
    connection.putheader('Transfer-Encoding', 'chunked')
    connection.putheader('Content-Type', 'audio/x-pcm;bit=16;rate=16000')
    connection.endheaders()

    log("Отправка записи")
    for chunk in chunks:
        connection.send(('%s\r\n' % hex(len(chunk))[2:]).encode())
        connection.send(chunk)
        connection.send('\r\n'.encode())

    connection.send('0\r\n\r\n'.encode())
    response = connection.getresponse()

    log("Обработка ответа сервера")
    if response.code == 200:
        response_text = response.read()
        xml = XmlElementTree.fromstring(response_text)

        if int(xml.attrib['success']) == 1:
            max_confidence = - float("inf")
            text = ''

            for child in xml:
                if float(child.attrib['confidence']) > max_confidence:
                    text = child.text
                    max_confidence = float(child.attrib['confidence'])

            if max_confidence != - float("inf"):
                return text
            else:
                raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
        else:
            raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
    else:
        raise SpeechException('Unknown error.\nCode: %s\n\n%s' % (response.code, response.read()))


def text_to_record(text, KEY, speaker='jane', emotion='neutral', speed=1.0):
    log("Преобразование текста в речь")
    filename = 'anek.mp3'
    url = 'https://tts.voicetech.yandex.net/generate?text={text}&format=mp3&lang=ru-RU&speaker=jane&key={key}&speaker={speaker}&emotion={emotion}&speed={speed}'.format(
        text=urllib.parse.quote(text),
        key=KEY, speaker=speaker, emotion=emotion, speed=speed)
    print("got_url")
    urllib.request.urlretrieve(url, 'tts/' + filename)
    print('got audio')
    return 'tts/' + filename


class SpeechException(Exception):
    pass
