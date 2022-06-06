import pandas as pd
from sqlalchemy import false

import App.DB.tsDB as db
import App.Engine.Engines as e
import App.Services.Services as srv
import App.Strategies.Strategies as s

dbConn = db.dbConnect()

algo = "S001-01-ORB-OpeningRangeBreakout"
symbol = "BANKNIFTY-FUT"
# date = "2022-05-20"
date = "2022-06-06"

df = s.execute(dbConn, algo + '-entr', symbol, date, False,
               False)  # get all entry calls
print(df)

df = s.execute(dbConn, algo + '-exit', symbol, date, False,
               False)  # get all entry calls
print(df)
