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

from utils import init_db, load_Channels, save_Channel, save_Channels, save_Message
# Telegram API credentials (get from my.telegram.org)

load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

# Telegram client
client = TelegramClient('sessions/anon.session', api_id, api_hash)

# List of channels to monitor (usernames or IDs)
channels = []
channels_ids = set()
# Cola para mensajes
messages = []

# Flask app
app = Flask(__name__)
socketio = SocketIO(app,async_mode='threading')

#Function for new message
@client.on(events.NewMessage)
async def my_event_handler(event ):
    chat = await event.get_chat()
    #print(chat)
    msg = Message(mensaje=event.raw_text, channel={chat.username}, date=str(event.date), autor=event.sender_id, message_id=event.id)
    channel_id = chat.id
    #print(msg.__str__())
    #print("Message from: ", chat.username)
    print("Este el id del canal: ", channel_id)
    if (channel_id in channels_ids ):
        print("Message added")
        messages.append(msg)
        #save_Message(msg)
        socketio.emit('new_message', msg.__dict__)
    
def run_telegram_client():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client.start(phone)
        client.run_until_disconnected()
    except Exception as e:
        print(f"Error al iniciar el cliente de Telegram: {e}")

# Evento de conexión de SocketIO
@socketio.on('connect')
def handle_connect():
    print("Cliente conectado")
    for msg in messages:
        emit('new_message', msg.__dict__)

# Update channel active
@socketio.on('update_channel_active')
def handle__update_channel_active(data):
    channel_id = data['id']
    active = data['active']
    try:
        if active:
            channels_ids.add(channel_id)
        else:
            channels_ids.remove(channel_id)
    except Exception as e:
        print(f"Error al actualizar el estado del canal: {e}")
    for channel in channels:
        if str(channel.id) == str(channel_id):
            channel.active = active
            print("Channel ", channel.name, " updated")
            break
        save_Channel(channel)
        
# Load channels
def loadChannels():
    rows = load_Channels()
    for row in rows:
        channel = Channel(id= row['channel_id'],name=row['name'], active=row['active'])
        channels.append(channel) 
        if channel.active:
            channels_ids.add(channel.name)

@app.route('/select_channels')
def select_channels():
    return render_template('select_channels.html')    

@app.route('/')
def index():
    return render_template("index.html", messages = messages, channels = channels)    

if __name__ == '__main__': 
    init_db()
    loadChannels()
    telegram_thread = threading.Thread(target=run_telegram_client, daemon=True)
    telegram_thread.start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
