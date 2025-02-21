import asyncio
import os
from telethon import TelegramClient, events
from kafka import KafkaProducer
from dotenv import load_dotenv

from classes.message import Message

# Telegram API credentials (get from my.telegram.org)

load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')


# Telegram client
client = TelegramClient('sessions/anon.session', api_id, api_hash)

# List of channels to monitor (usernames or IDs)
channels = ['cointelegraph', 'criptonoticias', 'news_crypto']


@client.on(events.NewMessage)
async def my_event_handler(event ):
    chat = await event.get_chat()
    print(chat)
    msg = Message(mensaje=event.raw_text, channel=f"{event.chat_id} : {chat.first_name}", date=event.date, autor=event.sender_id, message_id=event.id)
    print(msg.__str__())
    
    
client.start()
client.run_until_disconnected()