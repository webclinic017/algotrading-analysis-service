import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from App.Strategies import Strategies
from App.Engine import Engines
from App.Services import Services
from App.DB import tsDB


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


env = tsDB.envVar()
app = FastAPI()
dbConn = tsDB.dbConnect(env)
tsDB.createAllTables(dbConn)


@app.get("/")
def read_root():
    return {
        "Info":
        "algotrading-analysis-service v0.1.9-beta (Rel Date: 09-June-2022) [00]"
    }


@app.get("/services/")
def read_item(sid: str, date: Optional[str] = None):
    return Services.execute(env, dbConn, sid, date)


@app.get("/tradesignals/")
def read_item(algo: str, symbol: str, date: str):
    return Strategies.execute(env, dbConn, algo, symbol, date, True)


@app.get("/simulation/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = Strategies.execute(env, algo)
    return {"signals": ret}


@app.get("/active-trades/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = Engines.execute(env, dbConn, algo)
    return {"signals": ret}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
