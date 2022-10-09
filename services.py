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


# async def retrieve_min_max_trades(symbol: str, start_date: str, end_data: str):
#     trades = []
#     one_trade = await trades_collection.find_one({"symbol": symbol})
#
#     if not one_trade:
#         return "An error occurred", f"Сделок с символом {symbol} не существует", 404
#     one_trade_by_date = await trades_collection.find_one(
#         {"symbol": symbol, "timestamp": {'$gte': start_date, '$lte': end_data}})
#
#     if not one_trade_by_date:
#         return "An error occurred", f"Нет сделок в заданном периоде", 404
#
#     trades_aggregate = trades_collection.aggregate([
#         {"$match": {
#             "symbol": symbol,
#             'timestamp':
#                 {
#                     '$gte': start_date,
#                     '$lte': end_data
#                 }
#         }
#         },
#         {"$group": {
#             "_id": "$symbol",
#             "max": {"$max": "$price"},
#             "min": {"$min": "$price"}
#         }}])
#
#     async for trade in trades_aggregate:
#         trades.append(trade)
#     return trades
