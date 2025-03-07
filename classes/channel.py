class Channel():
    def __init__(self,id:str,name: str, active: bool) -> None:
        self.name = name
        self.id = id
        self.active = active
        #Añadir miembros o otros datos relevantes del canal
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active
        }