from db import trades_collection


async def add_trade(student_data: dict) -> dict:
    trade = await trades_collection.insert_one(student_data)
    new_trade = await trades_collection.find_one({"_id": trade.inserted_id})
    return trades_helper(new_trade)


async def retrieve_trades() -> list:
    trades = []
    async for trade in trades_collection.find():
        trades.append(trades_helper(trade))
    return trades


async def retrieve_trades_by_id_user(id: str):
    trades = []
    async for trade in trades_collection.find({"user.id": int(id)}):
        trades.append(trades_helper(trade))
    return trades


async def delete_all_trades() -> bool:
    await trades_collection.delete_many({})
    return True


async def retrieve_min_max_trades(symbol: str, start_date: str, end_data: str):
    trades = []
    trades_aggregate = trades_collection.aggregate([
        {"$match": {
            "symbol": symbol,
            'timestamp':
                {
                    '$gte': start_date,
                    '$lte': end_data
                }
        }
        },
        {"$group": {
            "_id": "$symbol",
            "MaximumValue": {"$max": "$price"},
            "MinimumValue": {"$min": "$price"}
        }}])

    async for trade in trades_aggregate:
        trades.append(trade)
    trades[0]["symbol"] = symbol
    return trades[0]


def trades_helper(trade) -> dict:
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
