import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tiktoken import main_token

vk_session = vk_api.VkApi(token=main_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def sender(id, text):
    vk.messages.send(user_id=id, message=text, random_id=0)


def send_sticker(id, number):
    vk.messages.send(user_id=id, sticker_id=number, random_id=0)


def send_photo(id, text, url):
    vk.messages.send(user_id = id, message = text, attachment = url, random_id = 0)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            msg = event.text.lower()
            id = event.user_id

            if msg == 'привет':
                sender(id, 'Привет')
                send_sticker(id, 19418)
            if msg == 'стикер':
                send_sticker(id, 19418)
            if msg == 'фото':
                send_photo(id, 'photo-203492759_457239018', 'photo-203492759_457239018')
