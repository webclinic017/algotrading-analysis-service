import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from App.Strategies import Strategies
from App.Engine import Engines
from App.DB import tsDB


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


app = FastAPI()
dbConn = tsDB.dbConnect()
tsDB.createAllTables(dbConn)


@app.get("/tradesignals/")
def read_item(algo: str):
    ret = Strategies.execute(dbConn, algo)
    return {"signals": ret}


@app.get("/simulation/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = Strategies.execute(algo)
    return {"signals": ret}


@app.get("/active-trades/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = Engines.execute(dbConn, algo)
    return {"signals": ret}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
