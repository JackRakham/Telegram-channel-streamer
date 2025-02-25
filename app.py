from queue import Queue
import json
from flask import Flask, render_template, jsonify, request, url_for
import asyncio
import os
from telethon import TelegramClient, events
from kafka import KafkaProducer
from dotenv import load_dotenv
import threading
from classes.channel import Channel
from classes.message import Message
from flask_socketio import SocketIO, emit

from utils import init_db, load_Channels, save_Channels
# Telegram API credentials (get from my.telegram.org)

load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

# Telegram client
client = TelegramClient('sessions/anon.session', api_id, api_hash)

# List of channels to monitor (usernames or IDs)
channels = []
channels_names = set()
# Cola para mensajes
messages = []

# Flask app
app = Flask(__name__)
socketio = SocketIO(app)

#Function for new message
@client.on(events.NewMessage)
async def my_event_handler(event ):
    chat = await event.get_chat()
    print(chat)
    msg = Message(mensaje=event.raw_text, channel=f"{event.chat_id} : {chat.username}", date=str(event.date), autor=event.sender_id, message_id=event.id)
    print(msg.__str__())
    if (chat.username in channels_names):
        messages.append(msg)
        socketio.emit('new_message', msg.__dict__)
    
def run_telegram_client():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client.start()
        client.run_until_disconnected()
    except Exception as e:
        print(f"Error al iniciar el cliente de Telegram: {e}")

# Evento de conexión de SocketIO
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado")
    for msg in messages:
        emit('new_message', msg.__dict__)

# Event for creating channel
@socketio.on('add_channel')
def handle_add_channel(data):
    channel_name = data['name']
    new_channel = Channel(name=channel_name, active=True)
    channels.append(new_channel)
    channels_names.add(channel_name)
    save_Channels(channels)
    socketio.emit('channel_added', {'url': url_for('index')})

# Update channel active
@socketio.on('update_channel_active')
def handle__update_channel_active(data):
    channel_name = data['name']
    active = data['active']
    if active:
        channels_names.add(channel_name)
    else:
        channels_names.remove(channel_name)
        
# Load channels
def loadChannels():
    rows = load_Channels()
    for row in rows:
        channel = Channel(name=row['name'], active=row['active'])
        channels.append(channel) 
        if channel.active:
            channels_names.add(channel.name)

@app.route('/')
def index():
    return render_template("index.html", messages = messages, channels = channels)    

if __name__ == '__main__': 
    init_db()
    loadChannels()
    telegram_thread = threading.Thread(target=run_telegram_client, daemon=True)
    telegram_thread.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
