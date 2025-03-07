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
from classes.message_Queue_Manager import MessageQueueManager
from utils import init_db, get_Channels, save_Channel
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
queue_manager = MessageQueueManager()


# Flask app
app = Flask(__name__)

#Function for new message
@client.on(events.NewMessage)
async def my_event_handler(event):
    chat = await event.get_chat()
    channel_id = chat.id
    try:
        msg = Message(
            mensaje=event.raw_text,
            channel=chat.title if chat.title else "No title",
            date=str(event.date),
            autor=str(event.sender_id),
        )
        formatted_channel_id = str("-100" + str(channel_id))
        print(f"Checking channel: {formatted_channel_id} in {channels_ids}")
        if formatted_channel_id in channels_ids:
            print("Message added")
            queue_manager.add_message(msg)
    except Exception as e:
        print(f"Error al guardar mensaje: {e}")

def run_telegram_client():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client.start()
        client.run_until_disconnected()
    except Exception as e:
        print(f"Error al iniciar el cliente de Telegram: {e}")

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages_list = queue_manager.get_all_messages()
    messages_list_local = [msg.__dict__() for msg in messages_list]
    print(f"Messages mirror queue size (get_messages): {queue_manager.messages_mirror_queue.qsize()}")
    print(f"Tamaño lista original: {len(messages_list)}")
    print(f"Tamaño lista devuelta: {len(messages_list_local)}")
    return jsonify(messages_list_local)

# Update channel active
@app.route('/update_channel_active', methods=['POST'])
def update_channel_active():
    data = request.get_json()
    channel_id = data.get('id')
    active = data.get('active')
    try:
        if active:
            channels_ids.add(channel_id)
        else:
            channels_ids.remove(channel_id)
        # Actualizar el estado del canal en la lista y la base de datos
        for channel in channels:
            if str(channel.id) == str(channel_id):
                channel.active = active
                print(f"Channel {channel.name} updated")
                save_Channel(channel)
                break
        
        return jsonify({"status": "success", "message": "Channel updated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
        
# Load channels
def loadChannels():
    rows = get_Channels()
    for row in rows:
        channel = Channel(id= row['channel_id'],name=row['name'], active=row['active'])
        channels.append(channel) 
        if channel.active:
            channels_ids.add(str(channel.id))

@app.route('/')
def index():
    return render_template("index.html", channels = channels)

def run_kafka_producer():
    producer = KafkaProducer({'bootstrap.servers': 'localhost:9092'})
    while True:
        try:
            msg = queue_manager.messages.get(block=True, timeout=1)
            msg_dict = msg.__dict__
            msg_json = json.dumps(msg_dict)
            producer.produce('social_media_messages', key=msg.channel, value=msg_json)
            producer.flush()
            print(f"Sent message to Kafka: {msg_json}")
        except Exception as e:
            print(f"Error al enviar mensaje a Kafka: {e}")
            

if __name__ == '__main__': 
    init_db()
    loadChannels()
    telegram_thread = threading.Thread(target=run_telegram_client,daemon=True)
    telegram_thread.start()
    app.run( debug=False, host='0.0.0.0', port=5000)
