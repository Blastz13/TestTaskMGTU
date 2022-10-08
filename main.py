from fastapi import FastAPI, APIRouter
from fastapi.encoders import jsonable_encoder

from schemas import CreateTradeSchema
from services import *

app = FastAPI()
trade_router = APIRouter(prefix="/trade", tags=["Trade"])
app.include_router(trade_router)


def ResponseModel(data=[], message=""):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


@app.post("/", response_description="Trades data added into the database")
async def add_trade_data(trade: CreateTradeSchema):
    trade_data = jsonable_encoder(trade)
    new_trade = await add_trade(trade_data)
    return ResponseModel(new_trade, "Trade added successfully.")


@app.get("/list", response_description="Trades retrieved")
async def get_list_trades():
    students = await retrieve_trades()
    if students:
        return ResponseModel(students, "Trades data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


@app.delete("/", response_description="Trades data deleted from the database")
async def delete_all_trades_data():
    deleted_student = await delete_all_trades()
    if deleted_student:
        return ResponseModel([], "Trades deleted successfully"
        )
    return ErrorResponseModel(
        "Error", 404, "Trades doesnt exist".format(id)
    )


@app.get("/{id}", response_description="Trades retrieved by id")
async def get_trades_data_by_id(id: str):
    trades = await retrieve_trades_by_id_user(id)
    if trades:
        return ResponseModel(
            trades, "Trades retrieved by id successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Trades with id {0} doesn't exist".format(id)
    )


@app.get("/stocks/{symbol}/price", response_description="Trades get min/max")
async def get_max_min_price(symbol: str, start_date: str, end_data: str):
    trades = await retrieve_min_max_trades(symbol, start_date, end_data)
    if trades:
        return ResponseModel(
            trades, "Trades get min/max successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Error".format(id)
    )
