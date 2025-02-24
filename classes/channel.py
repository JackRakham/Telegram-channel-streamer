class Channel():
    def __init__(self,name, url, active: bool) -> None:
        self.name = name
        self.url = url
        self.log = []
        self.active = active
        #Añadir miembros o otros datos relevantes del canal
        
    def to_dict(self):
        return {
            "name": self.name,
            "last_message": self.last_message,
            "url": self.url
        }