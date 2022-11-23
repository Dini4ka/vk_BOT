from config import *
import vk_api, vk
from pprint import pprint
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id


def write_msg(sender, message):
    auth.method('messages.send', {'chat_id': sender, 'message': message, 'random_id': get_random_id()})


def getByConversationMessageId(peer_id, conversation_message_ids, group_id):
    return auth.method('messages.getByConversationMessageId', {'peer_id': peer_id,
                                                               'conversation_message_ids': conversation_message_ids,
                                                               'group_id': group_id})


def pin_msg(peer_id, conversation_message_ids):
    auth.method('messages.pin', {'peer_id': peer_id,
                                 'conversation_message_id': conversation_message_ids})


def get_user(user_id):
    full_name = auth.method('users.get', {'user_ids': user_id})[0]
    return {'first_name': full_name['first_name'], 'last_name': full_name['last_name']}



auth = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(auth, group_id=group_id)
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != '':
        text_message = event.message.get('text')
        print(event)
        if 'bot_help' in text_message:
            conv_msg_id = event.obj['message']['conversation_message_id']
            peer_id = event.obj['message']['peer_id']
            sender = event.chat_id
            write_msg(sender, text_message)
            bot_conv_msg_id = conv_msg_id + 1
            pin_msg(peer_id, bot_conv_msg_id)
        try:
            if event.obj['message']['reply_message']['conversation_message_id'] == bot_conv_msg_id:
                full_name = get_user(event.obj['message']['from_id'])
                write_msg(sender, 'это был ответ на мое сообщение, на него ответил ' +
                          full_name['first_name'] + ' ' + full_name['last_name'])
        except Exception as ex:
            print(ex.args)
            continue
