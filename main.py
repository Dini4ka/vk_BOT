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


def pin_msg(peer_id, conversation_message_id,text):
    auth.method('messages.pin', {'peer_id': peer_id,
                                 'conversation_message_id': conversation_message_id})
    new_text = text.removesuffix('bot_help')
    edit_text = new_text + '<br>_________________________<br>' \
                          '_________________________<br>' \
                          'СПАСИБО ЗА ОБРАТНУЮ СВЯЗЬ'
    auth.method('messages.edit', {'peer_id': peer_id,
                                  'conversation_message_id': conversation_message_id,
                                  'message':edit_text})
    lego = [new_text,'<br>_________________________<br>','<br>_________________________<br>','СПАСИБО ЗА ОБРАТНУЮ СВЯЗЬ']
    return lego

def get_user(user_id):
    full_name = auth.method('users.get', {'user_ids': user_id})[0]
    return full_name['first_name'] + ' ' + full_name['last_name']


def edit_msg(peer_id,conversation_message_id,lego,plus,minus):
    plus_str = ''
    for positive in plus:
        plus_str += str(positive) + ' +' '<br>'
    minus_str = ''
    for negative in minus:
        minus_str += str(negative) + ' -' + '<br>'
    message = str(lego[0]) + lego[1] + plus_str + lego[2] + lego[3] + '<br>' + minus_str
    auth.method('messages.edit', {'peer_id': peer_id,
                                  'conversation_message_id': conversation_message_id,
                                  'message': message})


auth = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(auth, group_id=group_id)
TEXT = None
plus = []
minus = []
pinned_message = None
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
            lego = pin_msg(peer_id, bot_conv_msg_id, text_message)
        try:
            if event.obj['message']['reply_message']['conversation_message_id'] == bot_conv_msg_id:
                full_name = get_user(event.obj['message']['from_id'])
                if text_message == '+':
                    plus.append(full_name)
                    edit_msg(peer_id,bot_conv_msg_id,lego,plus,minus)
                if text_message == '-':
                    minus.append(full_name)
                    edit_msg(peer_id, bot_conv_msg_id, lego, plus, minus)
        except Exception as ex:
            print(ex.args)
            continue
