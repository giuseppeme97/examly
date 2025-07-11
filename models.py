from pydantic import BaseModel


class BaseRequest(BaseModel):
    source: str


class CompleteRequest(BaseModel):
    source: str
    filters: dict
    options: dict
