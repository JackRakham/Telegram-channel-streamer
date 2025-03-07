
from queue import Queue
import threading


class MessageQueueManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(MessageQueueManager, cls).__new__(cls)
                    # Inicializar las colas y la lista
                    cls._instance.messages = Queue()
                    cls._instance.messages_mirror_queue = Queue()
                    cls._instance.messages_list = []
                    print("Singleton MessageQueueManager inicializado")
        return cls._instance

    def add_message(self, msg):
        """Añadir un mensaje a ambas colas y actualizar la lista."""
        self.messages.put(msg)
        self.messages_mirror_queue.put(msg)
        print(f"Messages queue size: {self.messages.qsize()}")
        print(f"Messages mirror queue size: {self.messages_mirror_queue.qsize()}")

    def get_all_messages(self):
        """Obtener todos los mensajes de la cola espejo y añadirlos a la lista."""
        while not self.messages_mirror_queue.empty():
            self.messages_list.append(self.messages_mirror_queue.get())
        return self.messages_list