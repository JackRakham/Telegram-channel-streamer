
import os
from telethon import TelegramClient
import sqlite3
from dotenv import load_dotenv

from classes.channel import Channel

# Telegram API credentials (get from my.telegram.org)

load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

# Telegram client
client = TelegramClient('sessions/anon.session', api_id, api_hash)
client.start(phone=phone)

def get_db_connection():
    conn = sqlite3.connect('telegram_scraper.db', check_same_thread=False)  # check_same_thread=False para Flask-SocketIO
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

async def get_channels():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels")
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel:
            cursor.execute("INSERT INTO channels (channel_id, name, active) VALUES (?, ?, ?)", (dialog.id, dialog.title, False))
            print(dialog.id, dialog.title)
    conn.commit()
    cursor.close()
    conn.close()

with client:
    client.loop.run_until_complete(get_channels())