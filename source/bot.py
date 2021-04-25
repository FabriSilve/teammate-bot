import requests
from re import search
import base64
from bottle import run, post, response, request as bottle_request

# TODO: move in env variables
TOKEN = 'xxx'
ALLOW_RELOADING = True
IS_DEBUG = True
PORT = 8080
HOST = 'localhost'
SECRET = 'secret'
ALLOWED_CHAT_IDS = '244386202' # Add validation for allowed chats
# ALLOWED_CHAT_IDS = '111'

ADMIN_CHAT = '244386202'

BOT_URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)


# Call /subscribe to begin the integration. We will setup the credentials for you and notify you as soon as possible.
START = """
*TeamMate* is an api proxy to your Telegram's chat.
We will open a secure hook only for your chat and you will be able to receive messages from your applications.

Call /credentials to visualise the url you will need to use and you *unique* token.

*This Bot is Database free and we will not store anything from the messages you will send.*

Call /support if you have any question!
`/support How can I use your hook?`

Thank you and enjoy integrating with us!
"""

PRIVATE_SENDER_TEMPLATE = """
ChatID: {}
Username: @{}
"""

GROUP_SENDER_TEMPLATE = """
ChatID: {}
Username: @{}
Group: {}
"""

UKNOW_SENDER_TEMPLATE = """
ChatID: {}
Unkown type: {}
"""

# def encode(key, string):
#     encoded_chars = []
#     for i in xrange(len(string)):
#         key_c = key[i % len(key)]
#         encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
#         encoded_chars.append(encoded_c)
#     encoded_string = "".join(encoded_chars)
#     return base64.urlsafe_b64encode(encoded_string)

def get_token(chat_id):
    print(chat_id)
    string_bytes = str(chat_id).encode('ascii')
    print(string_bytes)
    base64_bytes = base64.b64encode(string_bytes)
    print(base64_bytes)
    base64_string = base64_bytes.decode('ascii')
    print(base64_string)
    return base64_string

def decode_token(token):
    base64_bytes = token.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    chat_id = message_bytes.decode('ascii')
    return chat_id

def get_chat_id(data):  
    chat_id = data['message']['chat']['id']

    return chat_id

def get_message(data):  
    message_text = data['message']['text']
    return message_text

def get_sender_details(data):
    chat_id = get_chat_id(data)
    chat = data['message']['chat']
    user = data['message']['from']
    chat_type = chat['type']

    if chat_type == 'private':
        return PRIVATE_SENDER_TEMPLATE.format(chat_id, user['username'])
    if chat_type == 'group':
        return GROUP_SENDER_TEMPLATE.format(chat_id, user['username'], chat['title'])

    return UKNOW_SENDER_TEMPLATE.format(chat_id, chat_type)

def get_credentials(chat_id):
    print('pre')
    token = get_token(chat_id)
    print('decoded')
    print(decode_token(token))
    url = '{}/hook/<TOKEN>'.format(HOST)

    return 'Your chat credentials:\nUrl: {}\nToken:{}'.format(url, token)

def send_message(chat_id, text):  
    message_url = BOT_URL + 'sendMessage'
    requests.post(
        message_url,
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": 'Markdown',
        },
    )


def process_message(data):
    chat_id = None
    message = None
    sender_details = None

    try:
        chat_id = get_chat_id(data)
        message = get_message(data)
        sender_details = get_sender_details(data)
    except:
        # Send error message to ERRORS chat
        return

    try: 
        print('here')
        print(message)
        if search("^/start", message):
            send_message(chat_id, START)
            admin_message = 'Command `/start` triggered.{}'.format(sender_details)
            send_message(ADMIN_CHAT, admin_message)
        # elif search("^/subscribe", message):
            # Subscribe command logic
        elif search("^/credentials", message):
            credentials_message = get_credentials(chat_id)
            print(credentials_message)
            send_message(chat_id, credentials_message)
        elif search("^/support", message):
            send_message(chat_id, 'Thank you. We will be back to you as soon as possible!')
            admin_message = 'Command `/support` triggered.{}\n{}'.format(sender_details, message)
            send_message(ADMIN_CHAT, admin_message)
            
        
    except:
        # Send error message to ERRORS_CHAT
        return

@post('/')  # our python function based endpoint
def main():
    data = bottle_request.json
    from pprint import pprint
    pprint(data)

    process_message(data)

    return response 

if __name__ == '__main__':  
    run(host=HOST, port=PORT, debug=IS_DEBUG, reloader=ALLOW_RELOADING)

    