import sqlite3

from classes.channel import Channel

# Crear tabla si no existe
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            author INTEGER,
            message_id INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            active BOOLEAN NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


# Función para obtener conexión a SQLite
def get_db_connection():
    conn = sqlite3.connect('telegram_scraper.db', check_same_thread=False)  # check_same_thread=False para Flask-SocketIO
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn

def save_Channels(channels):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM channels")
    for channel in channels:
        cursor.execute("INSERT INTO channels (channel_id, name, active) VALUES (?, ?, ?)", (channel.id, channel.name, channel.active))
    conn.commit()
    cursor.close()
    conn.close()

def save_Channel(channel):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE channels SET active = ? WHERE channel_id = ?", ( channel.active,channel.id))
    conn.commit()
    cursor.close()
    conn.close()

def save_Message(message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (channel, content, date, author, message_id) VALUES (?, ?, ?, ?, ?)", (message.channel, message.content, message.date, message.autor, message.message_id))
    conn.commit()
    cursor.close()
    conn.close()

def load_Channels():
    try:
        conn = sqlite3.connect('telegram_scraper.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT channel_id, name, active FROM channels")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Error: SQLite error - {e}")

def clear_Db():
    try:
        conn = sqlite3.connect('telegram_scraper.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT name, active FROM channels")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Error: SQLite error - {e}")
