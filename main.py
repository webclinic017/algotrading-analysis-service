import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from App.Strategies import Strategies
from App.Engine import Engines
from App.DB import tsDB
import pandas as pd


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


app = FastAPI()
dbConn = tsDB.dbConnect()
tsDB.createAllTables(dbConn)

# header_list = ['symbol', 'timestamp',\
#                    'Open', 'High', 'Low', 'Close', \
#                    'Null1', 'Null2', 'Null3', 'Null4']

# BNFs = pd.read_csv(
#     '/home/parag/devArea/algotrading-analysis-service/App/combined_bnf.csv',
#     header=None,
#     sep=',',
#     names=header_list)

# BNFs = BNFs.drop(columns=['Null1', 'Null2', 'Null3', 'Null4'])

# print(BNFs.head())
# print(BNFs.tail())

# print(BNFs.index.max() - BNFs.index.min())

# BNFs.to_csv(
#     '/home/parag/devArea/algotrading-analysis-service/App/combined_bnf_new.csv',
#     index=False)


@app.get("/tradesignals/")
def read_item(algo: str, symbol: str, date: str):
    return Strategies.execute(dbConn, algo, symbol, date)


@app.get("/simulation/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = Strategies.execute(algo)
    return {"signals": ret}


@app.get("/active-trades/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = Engines.execute(dbConn, algo)
    return {"signals": ret}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
