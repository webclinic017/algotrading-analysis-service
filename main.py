import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from  App.Strategies import StrategiesCaller

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


app = FastAPI()


@app.get("/analyse/{algo_id}")
def read_item(algo_id):
    StrategiesCaller.callStrategies()
    return {"item_id": algo_id}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)    