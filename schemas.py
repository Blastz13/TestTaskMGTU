from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    name: str


class CreateTradeSchema(BaseModel):
    type: str
    user: UserSchema
    symbol: str
    price: float
    timestamp: str
