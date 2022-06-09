import pandas as pd
from sqlalchemy import false

import App.DB.tsDB as db
import App.Engine.Engines as e
import App.Services.Services as srv
import App.Strategies.Strategies as s
import App.Libraries.lib_FN as libFn

env = db.envVar()
dbConn = db.dbConnect(env)

analysis_algorithm = "S001-01-ORB-OpeningRangeBreakout"
analysis_symbol = "BANKNIFTY-FUT"
analysis_duration_backward = '3 months'
analysis_end_date = ""  # "" for today

start, end = libFn.getDates(analysis_duration_backward, analysis_end_date)

# date = "2022-05-20"
# date = "2022-05-31"
# date = "2022-06-07"

df = s.execute(env, dbConn, algo + '-entr', symbol, date,
               False)  # get all entry calls
print(df)

df = s.execute(env, dbConn, algo + '-exit', symbol, date,
               False)  # get all entry calls
print(df)
