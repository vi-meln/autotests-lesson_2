import datetime

from pydantic import BaseModel


class Status(BaseModel):
    status: str
    timestamp: str
