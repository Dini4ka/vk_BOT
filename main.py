from config import *
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot_functions import *
from vk_api.utils import get_random_id

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
            plus = []
            minus = []
            conv_msg_id = event.obj['message']['conversation_message_id']
            peer_id = event.obj['message']['peer_id']
            sender = event.chat_id
            write_msg(auth,sender, text_message)
            bot_conv_msg_id = conv_msg_id + 1
            lego = pin_msg(auth,peer_id, bot_conv_msg_id, text_message)
        try:
            if event.obj['message']['reply_message']['conversation_message_id'] == bot_conv_msg_id:
                full_name = get_user(event.obj['message']['from_id'])
                if text_message == '+':
                    plus.append(full_name)
                    edit_msg(auth,peer_id, bot_conv_msg_id, lego, plus, minus)
                if text_message == '-':
                    minus.append(full_name)
                    edit_msg(auth,peer_id, bot_conv_msg_id, lego, plus, minus)
        except Exception as ex:
            print(ex.args)
            continue
