from asyncio import constants
import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from App.Strategies import Strategies
from App.Engine import Engines
from App.Services import Services
from App.DB import tsDB
import App.Services.backtesting as bt

LIVE_TRADING = True


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
        "algotrading-analysis-service v0.2.0-beta (Rel Date: 26-June-2022) [00]"
    }


@app.get("/services/")
def read_item(sid: str, date: Optional[str] = None):
    return Services.execute(env, dbConn, sid, date)


@app.get("/tradesignals/")
def read_item(
    mode: str,
    algo: str,
    symbol: str,
    date: str,
    pos_dir: Optional[str] = None,
    pos_entr_price: Optional[float] = None,
    pos_entr_time: Optional[str] = None,
):
    return Strategies.execute(env, dbConn, mode, algo, symbol, date,
                              pos_entr_price, pos_entr_time, LIVE_TRADING)


@app.get("/simulation/")
def read_item(analysis_algorithm: str = 'S001-01-ORB-OpeningRangeBreakout',
              analysis_symbol: str = "BANKNIFTY-FUT",
              analysis_duration_backward: str = "6 weeks",
              analysis_end_date: Optional[str] = None,
              plot_images: bool = False):

    ret = 2
    bt.backtesting(analysis_algorithm=analysis_algorithm,
                   analysis_symbol=analysis_symbol,
                   analysis_duration_backward=analysis_duration_backward,
                   analysis_end_date=analysis_end_date,
                   dbConn=dbConn,
                   env=env,
                   trading_mode=False,
                   plot_images=plot_images)
    return {"signals": ret}


@app.get("/active-trades/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = Engines.execute(env, dbConn, algo)
    return {"signals": ret}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
