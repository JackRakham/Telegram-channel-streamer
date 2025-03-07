# Telegram-channel-streamer

Application for gathering telegram channels messages in a kafka stream. You can edit and change what you want.

# 🚀 Features

✨ Telethon message gathering
🔹 Kafka Message streaming
🛠️ Flask UI for settings

📦 Technologies Used

* Flask
* Telethon
* Kafka

📜 Installation and Setup

1️⃣ Clone the repository
```sh
git clone https://github.com/JackRakham/Telegram-channel-streamer.git
cd Telegram-channel-streamer
```
2️⃣ Create and activate a virtual environment

  On Linux/macOS:
```sh
python3 -m venv venv
source venv/bin/activate
```
  On Windows:
```sh
python -m venv venv
venv\Scripts\activate
```
3️⃣ Install dependencies
```sh
pip install -r requirements.txt
```
4️⃣ Set up environment variables
```
API_ID = Get from your telegram app
API_HASH = Get from your telegram app
PHONE = You can use your own phone
```
5️⃣ Run the application
```python
python app.py
```
