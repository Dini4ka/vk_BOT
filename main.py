from config import *
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from bot_functions import *

# bot auth
auth = vk_api.VkApi(token=token)
# Process of reading messages
longpoll = VkBotLongPoll(auth, group_id=group_id)
# Text pinned message
TEXT = None
# Peoples answered in pinned message (only '+' or '-')
plus = []
minus = []

# Listening messages
for event in longpoll.listen():
    # If message was from VK chat and not empty
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != '':
        # Getting message's text
        text_message = event.message.get('text')
        print(event)
        # If message has a flag 'bot_help', we should reset plus and minus
        if 'bot_help' in text_message:
            plus = []
            minus = []
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
        # Processing another messages
        try:
            # If this is a reply to a bot message
            if event.obj['message']['reply_message']['conversation_message_id'] == bot_conv_msg_id:
                # Getting fullname of sender
                full_name = get_user(auth, event.obj['message']['from_id'])
                # if answer was '+'
                if text_message == '+':
                    plus.append(full_name)
                    edit_msg(auth, peer_id, bot_conv_msg_id, lego, plus, minus)
                # if answer was '-'
                if text_message == '-':
                    minus.append(full_name)
                    edit_msg(auth, peer_id, bot_conv_msg_id, lego, plus, minus)
            # if message isn't a reply to a bot message
        except Exception as ex:
            print(ex.args)
            continue
