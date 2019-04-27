import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import requests
import datetime
import json
import os
from vk_api import VkUpload
#import  change_voice_script
import urllib.request
import shutil
import yadisk

def downld(url, usr=''):
    file_name = url.split('/')[-1]
    # Download the file from `url` and save it locally under `file_name`:
    if ('mp3' in file_name):
        file_name = usr+'voice.mp3'
    else:
        file_name = usr+'gifka.gif'
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    out_file.close()
    return file_name



def write_msg(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'message': message,
        'random_id': random.randint(1, 9999)
    })

def write_vc(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'random_id': random.randint(1, 9999),
        'attachment': "doc" + message
    })

def write_photo(user_id, message):
    vk.method('messages.send', {
        'user_id': user_id,
        'random_id': random.randint(1, 9999),
        'message': "photo" + message,
        'attachment': "doc" + message
    })
def write_video(user_id):
    a = vk.method("video.save",{"name":"Stas.MOV"})
    vk.method('messages.send', {
        'user_id': user_id,
        'random_id': random.randint(1, 9999),
        'attachment': "video"+a["owner_id"] + '_' + a['vid']
    })



# yan_d = yadisk.YaDisk(token="AQAAAAAz2DAmAAWhKfyxW_mmgE0Todp1ZRFOm8E")
vk = vk_api.VkApi(token = "6e6e50ff9bb646bbbc7cf03d0a7fa7a21d22714ee7d0b2eae5ad9b69840d9ab9dbfc2bb6530773fb2d7be")
longpoll = VkLongPoll(vk)
session = requests.Session()
random.seed(version=2)
upload = VkUpload(vk)
url_gif = ''
url_audio_mes = ''
g, v = 0, 0
Greeting = ["Привет", "привет", "Здравствуй", "Хай", "Приветствую", "Доброго времени суток"]
Parting = ["Пока", "пока", "Бывай", "Удачи", "До скорого", "До свидания"]
v = {}
g = {}
# Основной цикл
for event in longpoll.listen():
    # Если пришло новое сообщение
    if (event.type == VkEventType.MESSAGE_NEW) and event.to_me:
        msg_type = 'None' # будем хранить тип сообщения
        uid = event.user_id
        if event.to_me:
            try:
        # Если оно имеет метку для меня( то есть бота)
                # Сообщение от пользователя
                if(list(event.attachments.items()) == []):
                    msg_type = "TextMessage"
                elif event.attachments['attach1_type'] == 'sticker':
                    msg_type = "Sticker"
                elif event.attachments['attach1_type'] == 'photo':
                    msg_type = "Photo"
                elif event.attachments['attach1_type'] == 'doc':
                    if  ('attach1_kind' in event.attachments):
                        msg_type = event.attachments['attach1_kind']
                    else:
                        msg_type = "GIF"
                print("type = " + msg_type)
            except KeyError:
                write_msg(event.user_id, "Что ты мне кинул?")
            if msg_type == "TextMessage":
                request = event.text
                if request in Greeting:
                    write_msg(event.user_id, random.choice(Greeting))
                elif request in Parting:
                    write_msg(event.user_id, random.choice(Parting))
                elif request == "Gif+MP3":
                    write_msg(event.user_id, "Видео")
                elif request == "Спасибо":
                    write_msg(event.user_id, "Приходите еще")
                    # try:
                    #     # yan_d.remove("Video/FINAL.avi")
                    # except yadisk.exceptions.PathNotFoundError:
                    #     print("The file is already deleted")
                else:
                    write_msg(event.user_id, "Я не понимаю, что Вы хотели мне сказать...\nЕсли хочешь получить классный видеоролик, то отправь мне выбранную GIF и голосовое, а остальное я сделаю сам\nGIF можно взять здесь\nhttps://gifer.com/ru/gifs/%D0%BF%D0%B8%D0%BA%D0%B0%D1%87%D1%83")
            elif msg_type == "audiomsg":
                write_msg(event.user_id, "Я тебя услышал")
                url_audio_mes = vk.method("messages.getById", {"message_ids": event.message_id})['items'][0]['attachments'][0]['audio_message']['link_mp3']
                v[uid] = 1
            elif msg_type == "GIF":
                write_msg(event.user_id, "Отличная GIF")
                url_gif = vk.method("messages.getById", {"message_ids": event.message_id})['items'][0]['attachments'][0]['doc']['url']
                g[uid] = 1
            elif msg_type == "Photo":
                write_msg(event.user_id, "Хорошая фотография, но  мне бы GIF...")
            elif msg_type == "Sticker":
                write_msg(event.user_id, "Стикеры это классно, но пока я не умею с ними работать...")
            else:
                write_msg(event.user_id, "Это не GIF")
        print('Я тут')
        if (url_audio_mes != ''):
            a_name = downld(url_audio_mes, usr=uid)
            v = 1
            url_audio_mes = ''
            print('Я скачал голос')
        if (url_gif != ''):
            g = 1;
            g_name = downld(url_gif, usr=uid)
            url_gif = ''
            print('Я скачал gif')
        if (v[uid] + g[uid] == 2):
            try:
                os.system("rm ../data/" + uid + "FINAL.avi")
            except:
                pass
            os.system("python3 create_f.py " + a_name + ' ' + g_name + ' ' + uid) # > dev/null ??? & subprocess       
            write_msg(event.user_id, "Ваше видео\n" + 'yra200111ruz.fvds.ru/data/' + uid + 'FINAL.avi')
            
            v, g = 0, 0
        
        print(g,' ', v)
