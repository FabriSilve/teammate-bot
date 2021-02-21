import requests  
from bottle import run, post, response, request as bottle_request

# TODO: move in env variables
TOKEN = 'xxx'
ALLOW_RELOADING = True
IS_DEBUG = True
PORT = 8080
HOST = 'localhost'
ALLOWED_CHAT_IDS = '111' 

BOT_URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)

def get_chat_id(data):  
    """
    Method to extract chat id from telegram request.
    """
    chat_id = data['message']['chat']['id']

    return chat_id


def get_message(data):  
    """
    Method to extract message id from telegram request.
    """
    message_text = data['message']['text']
    return message_text


def send_message(prepared_data):  
    """
    Prepared data should be json which includes at least `chat_id` and `text`
    """ 
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=prepared_data)

def prepare_data_for_answer(data):  
    answer = 'You said: {}'.format(get_message(data))

    print(get_chat_id(data))

    json_data = {
        "chat_id": get_chat_id(data),
        "text": answer,
    }

    return json_data

@post('/')  # our python function based endpoint
def main():
    data = bottle_request.json 
    
    answer_data = prepare_data_for_answer(data)
    send_message(answer_data)  # <--- function for sending answer

    return response 

if __name__ == '__main__':  
    run(host=HOST, port=PORT, debug=IS_DEBUG, reloader=ALLOW_RELOADING)

    