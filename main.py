from config import *
import vk_api,vk
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

def write_msg(sender,message):
    auth.method('messages.send',{'chat_id':sender,'message': message, 'random_id': get_random_id()})

auth = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(auth,group_id=group_id)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != '':
        reseived_message = event.message.get('text')
        sender = event.chat_id
        if reseived_message == 'Ты здесь ?':
            write_msg(sender,'Здесь')


