import vk_api
import json
import random
import webbrowser
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from data import *

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


def get_link_button():
    return {
        "action": {
            "type": "open_link",
            "link": "https://vk.com/id1",
            "label": "Ссылка",
            "payload": ""
        },
    }


keyboard = {
    "one_time": False,
    "buttons": [
        [get_button('Забрать доступ', 'secondary'), get_button('Дать доступ', 'secondary')],
        [get_button('Краши мейн', 'secondary'), get_button('Краши бот 1', 'secondary'),
         get_button('Краши бот 2', 'secondary')], [get_link_button()]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def sender(id, text):
    vk.messages.send(user_id=id, message=text, random_id=get_random_id(), keyboard=keyboard)


def send_sticker(id, number):
    vk.messages.send(user_id=id, sticker_id=number, random_id=0)


def send_photo(id, text, url):
    vk.messages.send(user_id=id, message=text, attachment=url, random_id=0)


def greet():
    greetings_message = greetings_list[random.randint(0, len(greetings_list) - 1)]
    sender(id, greetings_message)
    send_sticker(id, 8472)


def beta_report_decision():
    verdict_message = statuses[random.randint(0, len(statuses) - 1)]
    sender(id, verdict_message)


def openBrowser(url):
    webbrowser.open(url)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            msg = event.text.lower()
            id = event.user_id

            if msg == 'привет':
                greet()
            elif msg == 'стикер':
                send_sticker(id, 19418)
            elif msg == 'фото?':
                send_photo(id, '', 'photo-203492759_457239018')
            elif msg == 'бот 1':
                sender(id, '641688889')
            elif msg == 'бот 2':
                sender(id, '641688892')
            elif msg == 'краши мейн':
                openBrowser(main_crushes)
            elif msg == 'краши бот 1':
                openBrowser(bot1_crushes)
            elif msg == 'краши бот 2':
                openBrowser(bot2_crushes)
            elif msg == 'забрать доступ':
                sender(id, revoke_list)
            elif msg == 'дать доступ':
                sender(id, grant_list)
            elif msg == 'спасибо':
                sender(id, 'Пожалуйста')
            elif msg == 'какой статус поставить репорту?':
                beta_report_decision()
            elif msg == 'переговорки':
                sender(id, meeting_rooms)
            elif msg == 'открой':
                openBrowser()
            else:
                sender(id, 'Я вас не понял')
