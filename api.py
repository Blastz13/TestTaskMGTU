from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from schemas import CreateTradeSchema
from services import *

trade_router = APIRouter(prefix="/trade", tags=["Trade"])


@trade_router.post("/", response_description="Trades data added into the database")
async def add_trade_data(trade: CreateTradeSchema):
    trade_data = jsonable_encoder(trade)
    new_trade = await add_trade(trade_data)
    return JSONResponse(response_model(new_trade, "Trade added successfully."), 201)


@trade_router.get("/list", response_description="Trades retrieved")
async def get_list_trades():
    trades = await retrieve_trades()
    if trades:
        return JSONResponse(response_model(trades, "Trades data retrieved successfully"), 200)
    return JSONResponse(response_model(trades, "Empty list returned"), 204)


@trade_router.delete("/delete", response_description="Trades data deleted from the database")
async def delete_all_trades_data():
    deleted_trades = await delete_all_trades()
    if deleted_trades:
        return JSONResponse(response_model([], "Trades deleted successfully"), 200)
    return JSONResponse(response_model([], "Trades doesnt exist".format(id)), 404)


@trade_router.get("/{id}", response_description="Trades retrieved by id")
async def get_trades_data_by_id_user(id: str):
    trades = await retrieve_trades_by_id_user(id)
    if trades:
        return JSONResponse(response_model(trades, "Trades retrieved by id successfully"), 200)
    return JSONResponse(response_model("An error occurred", "Trades with id {0} doesn't exist".format(id)), 404)


@trade_router.get("/stocks/{symbol}/price", response_description="Trades get min/max")
async def get_max_min_price(symbol: str, start_date: str, end_data: str):
    trades = []
    one_trade = await trades_collection.find_one({"symbol": symbol})

    if not one_trade:
        return JSONResponse(response_model("An error occurred", f"Сделок с символом {symbol} не существует"), 404)
    one_trade_by_date = await trades_collection.find_one(
        {"symbol": symbol, "timestamp": {'$gte': start_date, '$lte': end_data}})

    if not one_trade_by_date:
        return JSONResponse(response_model("An error occurred", f"Нет сделок в заданном периоде"), 404)

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
            "max": {"$max": "$price"},
            "min": {"$min": "$price"}
        }}])

    async for trade in trades_aggregate:
        trades.append(trade)

    if trades:
        return JSONResponse(response_model(trades, "Trades get min/max successfully"), 200)
    return JSONResponse(response_model("An error occurred", "Error".format(id)), 404)
