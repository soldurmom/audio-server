import asyncio
import json
import time
import requests
import urllib

from config import config


TOKEN = config.BOT_TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
USERNAME_BOT = "soldurmomBot"


async def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


async def get_json_from_url(url):
    content = await get_url(url)
    js = json.loads(content)
    return js


async def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = await get_json_from_url(url)
    return js


async def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


async def echo_all(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                print(text)

                if text == "/test" or text == "/test@" + USERNAME_BOT:
                    text = "test response"
                    await send_message(text, chat)
                elif text == "/start" or text == "/start@" + USERNAME_BOT:
                    await send_message("/test for test the bot", chat)


async def send_message(text, chat_id):
    tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    await get_url(url)


async def main():
    last_update_id = None
    while True:
        updates = await get_updates(last_update_id)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = await get_last_update_id(updates) + 1
                await echo_all(updates)
        time.sleep(5)

asyncio.run(main())

print('after main')
