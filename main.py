from config import *
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot_functions import *

import time

# Text pinned message
TEXT = None
# Peoples answered in pinned message (only '+' or '-')
plus = []
minus = []
plus_minus = []
# conversation_message_id pinned msg
bot_conv_msg_id = None
while True:
    try:
        # bot auth
        auth = vk_api.VkApi(token=token)
        # Process of reading messages
        longpoll = VkBotLongPoll(auth, group_id=group_id)
        # Listening messages
        for event in longpoll.listen():
            print(event)
            # If message was from VK chat and not empty
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != '':
                # Getting message's text
                text_message = event.message.get('text')
                # If message has a flag 'bot_help', we should reset plus and minus
                if 'bot_help' in text_message and event.obj['message']['from_id'] == admin_id:
                    plus = []
                    minus = []
                    plus_minus =[]
                    # Getting inclusive message id in chat
                    conv_msg_id = event.obj['message']['conversation_message_id']
                    peer_id = event.obj['message']['peer_id']
                    # Getting inclusive chat_id
                    sender = event.chat_id
                    # Duplicate admin massage
                    write_msg(auth, sender, text_message)
                    # Pin message which duplicated
                    bot_conv_msg_id = conv_msg_id + 1
                    lego = pin_msg(auth, peer_id, bot_conv_msg_id, text_message)
                if 'bot_edit' in text_message and event.obj['message'][
                    'from_id'] == admin_id and bot_conv_msg_id != None:
                    lego[0] = text_message[:-8]
                    edit_msg(auth, peer_id, bot_conv_msg_id, lego, plus, minus, plus_minus)
                # Processing another messages
                try:
                    # If this is a reply to a bot message
                    if event.obj['message']['reply_message']['conversation_message_id'] == bot_conv_msg_id:
                        # Getting fullname of sender
                        full_name = get_user(auth, event.obj['message']['from_id'])
                        # if answer was '+'
                        if '+' in text_message and '+-' not in text_message and '-+' not in text_message:
                            if full_name in plus:
                                plus.remove(full_name)
                            if full_name in minus:
                                minus.remove(full_name)
                            if full_name in plus_minus:
                                plus_minus.remove(full_name)
                            plus.append(full_name)
                            edit_msg(auth, peer_id, bot_conv_msg_id, lego, plus, minus,plus_minus)
                        # if answer was '-'
                        if '-' in text_message and '+-' not in text_message and '-+' not in text_message:
                            if full_name in minus:
                                minus.remove(full_name)
                            if full_name in plus:
                                plus.remove(full_name)
                            if full_name in plus_minus:
                                plus_minus.remove(full_name)
                            minus.append(full_name)
                            edit_msg(auth, peer_id, bot_conv_msg_id, lego, plus, minus,plus_minus)
                        # if answer was '+-' or '-+'
                        if '+-' in text_message or '-+' in text_message:
                            if full_name in plus:
                                plus.remove(full_name)
                            if full_name in minus:
                                minus.remove(full_name)
                            if full_name in plus_minus:
                                plus_minus.remove(full_name)
                            plus_minus.append(full_name)
                            edit_msg(auth,peer_id,bot_conv_msg_id,lego,plus,minus,plus_minus)
                    # if message isn't a reply to a bot message
                except Exception as ex:
                    print(ex.args)
                    continue
    except Exception as ex:
        print(ex)
        print('\n Переподключерие к серверам ВК \n')
        time.sleep(5)