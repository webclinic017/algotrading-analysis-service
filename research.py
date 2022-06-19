import pandas as pd
from tqdm import tqdm
from time import sleep

import App.DB.tsDB as db
import App.Engine.Engines as e
import App.Services.Services as srv
import App.Strategies.Strategies as s
import App.Libraries.lib_FN as libFn
import App.Libraries.lib_BACKTEST as libBk

env = db.envVar()
dbConn = db.dbConnect(env)

analysis_algorithm = "S001-01-ORB-OpeningRangeBreakout"
analysis_symbol = "BANKNIFTY-FUT"
analysis_duration_backward = "1 month"
analysis_end_date = ""  # "" for today

start, end = libFn.getDates(analysis_duration_backward, analysis_end_date)

scan_dates = db.get_dates_list(dbConn, start, end)

result = pd.DataFrame(columns=None)

for dt in tqdm(scan_dates, colour="green"):

    df = s.execute(
        env, dbConn, analysis_algorithm + "-entr", analysis_symbol, dt, False
    )  # get all entry calls
    # print(df)
    result = result.append(df)

#  TODO: start loop over the analysed dates from entr signals

# df = s.execute(env, dbConn, analysis_algorithm + '-exit', analysis_symbol,
#                dt, False)  # get all entry calls
# print(df)

libBk.btResultsParser(
    result, analysis_algorithm, plot=True, duration=analysis_duration_backward
)
