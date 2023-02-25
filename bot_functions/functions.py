from vk_api.utils import get_random_id


# Pin message in chat
def pin_msg(auth, peer_id, conversation_message_id, text):
    auth.method('messages.pin', {'peer_id': peer_id,
                                 'conversation_message_id': conversation_message_id})
    # For python 3.9+
    # new_text = text.removesuffix('bot_help')
    # For python less than 3.9
    new_text = text[:-8]
    edit_text = new_text + '<br>_________________________<br>' \
                           '_________________________<br>' \
                           '_________________________<br>' \

    auth.method('messages.edit', {'peer_id': peer_id,
                                  'conversation_message_id': conversation_message_id,
                                  'message': edit_text})
    lego = [new_text,
            '<br>_________________________<br>',
            '<br>_________________________<br>',
            '<br>_________________________<br>',
    ]
    return lego


# Identify user
def get_user(auth, user_id):
    full_name = auth.method('users.get', {'user_ids': user_id})[0]
    return full_name['first_name'] + ' ' + full_name['last_name']


# Redact the message
def edit_msg(auth, peer_id, conversation_message_id, lego, plus, minus, plus_minus):

    # 'plus' messages
    plus_str = ''
    plus_int = str(len(plus)) + ' +'
    for positive in plus:
        plus_str += str(positive) + ' +' '<br>'

    # 'minus' messages
    minus_str = ''
    minus_int = str(len(minus)) + ' -'
    for negative in minus:
        minus_str += str(negative) + ' -' + '<br>'

    # 'plus-minus' messages
    neutral_str = ''
    plus_minus_int = str(len(plus_minus)) + ' +-'
    for neutral in plus_minus:
        neutral_str += str(neutral) + ' +-' + '<br>'
    message = str(lego[0]) + lego[1] + '<br>' + plus_int + '<br><br>' + plus_str + '<br>' + plus_int + '<br>' \
                           + lego[2] + '<br>' + plus_minus_int + '<br><br>' + neutral_str + '<br>' + plus_minus_int + '<br>' \
                           + lego[3] + '<br>' + minus_int + '<br><br>' + minus_str + '<br>' + minus_int + '<br>'
    auth.method('messages.edit', {'peer_id': peer_id,
                                  'conversation_message_id': conversation_message_id,
                                  'message': message})


# Write message in chat
def write_msg(auth, sender, message):
    auth.method('messages.send', {'chat_id': sender, 'message': message, 'random_id': get_random_id()})


# Get user's info using he's conversation_message_id
def getByConversationMessageId(auth, peer_id, conversation_message_ids, group_id):
    return auth.method('messages.getByConversationMessageId', {'peer_id': peer_id,
                                                               'conversation_message_ids': conversation_message_ids,
                                                               'group_id': group_id})
