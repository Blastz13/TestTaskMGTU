from pydantic import BaseModel


class CreateTradeSchema(BaseModel):
    id: int
    type: str
    user: int
    symbol: str
    price: float
    timestamp: str
