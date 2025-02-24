from queue import Queue
import json
from flask import Flask, render_template, jsonify, request
import asyncio
import os
from telethon import TelegramClient, events
from kafka import KafkaProducer
from dotenv import load_dotenv
import threading
from classes.channel import Channel
from classes.message import Message
from flask_socketio import SocketIO, emit
# Telegram API credentials (get from my.telegram.org)

load_dotenv()
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')


# Telegram client
client = TelegramClient('sessions/anon.session', api_id, api_hash)

# List of channels to monitor (usernames or IDs)
channels = ['cointelegraph', 'criptonoticias', 'news_crypto']

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
    msg = Message(mensaje=event.raw_text, channel=f"{event.chat_id} : {chat.first_name}", date=str(event.date), autor=event.sender_id, message_id=event.id)
    print(msg.__str__())
    if (chat.username in channels):
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
    # Enviar mensajes existentes al nuevo cliente (opcional)
    for msg in messages:
        emit('new_message', msg.__dict__)

# Load channels
def loadChannels():
    try:
        with open('data/channels.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            channels.clear()
            for item in data:
                channel = Channel(name=item['name'], url=item['url'], active=item['active'])
                channels.append(channel)
    except FileNotFoundError:
        print("Error: channels.json not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
    except KeyError as e:
        print(f"Error: Key error {e}")
    


@app.route('/')
def index():
    return render_template("index.html", messages= messages, channels = channels)    

if __name__ == '__main__': 
    loadChannels()
    telegram_thread = threading.Thread(target=run_telegram_client, daemon=True)
    telegram_thread.start()


    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
