from datetime import datetime

class Message:
    def __init__(self, content: str, channel: str, date: datetime, autor: str, type: str) -> None:
        self.content = content
        self.channel = channel
        self.date = date
        self.autor = autor
        self.type = type

    def __str__(self) -> str:
        return f"- Message:\n   Date: {self.date}\n   Message: {self.content}\n   Channel: {self.channel} \n   Autor: {self.autor}\n"

    @classmethod
    def from_json(cls, json_data: dict):
        date_str = json_data.get("date")
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S%z")
        
        return cls(
            channel=json_data.get("channel"),
            content=json_data.get("content"),
            date=date_obj,
            autor=json_data.get("autor"),
            type = json_data.get("type")
        )
