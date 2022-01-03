import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from  App.Strategies import StrategiesCaller
from App.Engine import EngineCaller

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


app = FastAPI()


@app.get("/tradesignals/")
def read_item(algo: str):
    ret = StrategiesCaller.execute(algo)
    return {"signals": ret}


@app.get("/simulation/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = StrategiesCaller.execute(algo)
    return {"signals": ret}

@app.get("/active-trades/")
def read_item(algo: str, symbol: str, startdate: str, enddate: str):
    ret = EngineCaller.execute(algo)
    return {"signals": ret}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)    