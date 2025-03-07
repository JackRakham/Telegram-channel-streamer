class Message():
    def __init__(self, mensaje: str, channel: str, date: str, autor: str, message_id: int) -> None:
        self.content = mensaje
        self.channel = channel
        self.date = date
        self.autor = autor
        self.message_id = message_id
        self.type = "Telegram"
        
    def __str__(self) -> str:
        return f"- Message:\n   Fecha: {self.date}\n   Mensaje: {self.content}\n   Canal: {self.channel} \n   Autor: {self.autor}\n"
        
        
    def __dict__(self):
        return {
            "content": self.content,
            "channel": self.channel,
            "date": self.date,
            "autor": self.autor,
            "message_id": self.message_id,
            "type": self.type
        }
