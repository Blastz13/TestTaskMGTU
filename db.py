import motor.motor_asyncio

MONGO_DETAILS = "mongodb://mongo_db:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.trades

trades_collection = database.get_collection("trades_collection")
