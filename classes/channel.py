class Channel():
    def __init__(self,name, last_message_id, url) -> None:
        self.name = name
        self.last_message = last_message_id
        self.url = url
        self.log = []
        #Añadir miembros o otros datos relevantes del canal
        
    def to_dict(self):
        return {
            "name": self.name,
            "last_message": self.last_message,
            "url": self.url
        }