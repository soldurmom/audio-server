import requests
import urllib
from config import config

TOKEN = config.BOT_TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def send_message(chat_id, text):
    tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    get_url(url)

def edit_message(chat_id, message_id, text):
    tot = urllib.parse.quote_plus(text)
    url = URL + "editMessage?text={}&chat_id={}&message_id={}".format(tot, chat_id, message_id)
    get_url(url)