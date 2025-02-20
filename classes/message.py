class Message():
    def __init__(self, mensaje: str, channel: str, date: str, autor: str, message_id: int) -> None:
        self.content = mensaje
        self.channel = channel
        self.date = date
        self.autor = autor
        self.message_id = message_id
        self.type = "Telegram"
        
    def __str__(self) -> str:
        return f"Fecha: {self.date}\nMensaje: {self.mensaje} \nCanal: {self.channel} \nAutor: {self.autor}"
        
        

