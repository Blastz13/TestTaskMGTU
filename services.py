from db import trades_collection


def response_model(data=None, message="") -> dict:
    if data is None:
        data = []
    return {
        "data": data,
        "message": message,
    }


def trades_helper(trade: dict) -> dict:
    print(trade)
    return {
        "id": str(trade["_id"]),
        "type": trade["type"],
        "user": {
                 "id": trade["user"]["id"],
                 "name": trade["user"]["name"]
                 },
        "symbol": trade["symbol"],
        "price": trade["price"],
        "timestamp": trade["timestamp"],
    }


async def add_trade(student_data: dict) -> dict:
    trade = await trades_collection.insert_one(student_data)
    new_trade = await trades_collection.find_one({"_id": trade.inserted_id})
    return trades_helper(new_trade)


async def retrieve_trades() -> list:
    trades = []
    async for trade in trades_collection.find():
        trades.append(trades_helper(trade))
    return trades


async def retrieve_trades_by_id_user(id: str) -> list:
    trades = []
    async for trade in trades_collection.find({"user.id": id}):
        trades.append(trades_helper(trade))
    return trades


async def delete_all_trades() -> bool:
    del_trades = await trades_collection.delete_many({})
    if del_trades:
        return True
    return False
