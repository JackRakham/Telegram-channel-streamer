class Message():
    def __init__(self, mensaje: str, channel: str, date: str, autor: str) -> None:
        self.content = mensaje
        self.channel = channel
        self.date = date
        self.autor = autor
        self.type = "Telegram"
        
    def __str__(self) -> str:
        return f"- Message:\n   Fecha: {self.date}\n   Mensaje: {self.content}\n   Canal: {self.channel} \n   Autor: {self.autor}\n"
        
        
    def __dict__(self):
        return {
            "content": self.content,
            "channel": self.channel,
            "date": self.date,
            "autor": self.autor,
            "type": self.type
        }
