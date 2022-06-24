import os
import pandas as pd
from tqdm import tqdm
from time import sleep

import App.DB.tsDB as db
import App.Engine.Engines as e
import App.Services.Services as srv
import App.Strategies.Strategies as s
import App.Libraries.lib_FN as libFn
import App.Libraries.lib_BACKTEST as libBk

SIMULATION = False

env = db.envVar()
dbConn = db.dbConnect(env)

analysis_algorithm = "S001-01-ORB-OpeningRangeBreakout"
analysis_symbol = "BANKNIFTY-FUT"
analysis_duration_backward = "6 month"
analysis_end_date = ""  # "" for today

start, end = libFn.getDates(analysis_duration_backward, analysis_end_date)

scan_dates = db.get_dates_list(dbConn, start, end)

result = pd.DataFrame(columns=None)

for dt in tqdm(scan_dates, colour="green"):

    df_entr = s.execute(env=env,
                        dbConn=dbConn,
                        mode="entr",
                        algoID=analysis_algorithm,
                        symbol=analysis_symbol,
                        date=dt,
                        pos_dir="",
                        pos_entr_price=0,
                        pos_entr_time="",
                        trading=SIMULATION)  # get all entry calls
    df_r = df_entr

    if df_entr.at[0, 'dir'] == 'Bullish' or df_entr.at[0, 'dir'] == 'Bearish':

        df_exit = s.execute(env=env,
                            dbConn=dbConn,
                            mode="exit",
                            algoID=analysis_algorithm,
                            symbol=analysis_symbol,
                            date=dt,
                            pos_dir=df_entr.at[0, 'dir'],
                            pos_entr_price=df_entr.at[0, 'entry'],
                            pos_entr_time=df_entr.at[0, 'date'],
                            trading=SIMULATION)  # get all exit calls

        df_r.at[0, "exit"] = df_exit.at[0, "exit"]
        df_r.at[0, "exit_time"] = df_exit.at[0, "exit_time"]
        df_r.at[0, "exit_reason"] = df_exit.at[0, "exit_reason"]

    result = result.append(df_r)

libBk.btResultsParser(result,
                      analysis_algorithm,
                      plot=True,
                      duration=analysis_duration_backward)
