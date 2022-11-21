from config import *
import vk_api, vk
from pprint import pprint
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


def write_msg(sender, message):
    auth.method('messages.send', {'chat_id': sender, 'message': message, 'random_id': get_random_id()})


auth = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(auth, group_id=group_id)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != '':
        text_message = event.message.get('text')
        if 'bot_help' in text_message:
            conv_msg_id = event.obj['message']['conversation_message_id']
            peer_id = event.obj['message']['peer_id']
            auth.method('messages.pin',{'peer_id': peer_id, 'conversation_message_id': conv_msg_id})
            sender=event.chat_id
            write_msg(sender,'Закрепил сообщение')