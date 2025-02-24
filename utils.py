import sqlite3

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
    conn.commit()
    cursor.close()
    conn.close()


# Función para obtener conexión a SQLite
def get_db_connection():
    conn = sqlite3.connect('telegram_scraper.db', check_same_thread=False)  # check_same_thread=False para Flask-SocketIO
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    return conn