from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str


class CreateTradeSchema(BaseModel):
    id: int
    type: str
    user: UserSchema
    symbol: str
    price: float
    timestamp: str
