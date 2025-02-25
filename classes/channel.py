class Channel():
    def __init__(self,name: str, active: bool) -> None:
        self.name = name
        self.active = active
        #Añadir miembros o otros datos relevantes del canal
        
    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active
        }