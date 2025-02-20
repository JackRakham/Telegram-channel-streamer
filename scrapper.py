import asyncio
import os
from telethon import TelegramClient
from kafka import KafkaProducer
from dotenv import load_dotenv

# Telegram API credentials (get from my.telegram.org)

load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

# Kafka setup
# kafka_broker = 'localhost:9092'  # Adjust to your Kafka server
# producer = KafkaProducer(
#     bootstrap_servers=kafka_broker,
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# Telegram client
client = TelegramClient('*/sessions/anon', api_id, api_hash)

# List of channels to monitor (usernames or IDs)
channels = ['channel1_username', 'channel2_username', 'channel3_username']

async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with
    print(me.stringify())

with client:
    client.loop.run_until_complete(main())