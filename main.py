from fastapi import FastAPI

from api import trade_router

app = FastAPI()

app.include_router(trade_router)
