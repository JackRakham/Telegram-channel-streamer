
from datetime import datetime


class Update():
    def __init__(self, asset: str, feeling: str, content: str, date: datetime, sourceType: str) -> None:
        self.asset = asset
        self.feeling = feeling
        self.content = content
        self.date = date
        self.sourceType = sourceType

    