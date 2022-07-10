from App.DB import tsDB
import App.Libraries.lib_CANDLES as libCdl

# import datetime
import pandas as pd
from glob import iglob
import App.DB.tsDB as db
import os
import sys


# Function works if called on next day,
# if called on same day, getCdlBtwnTime --> provdies ticks data - causing failure
# calling next day, reads form 1min table --> provide null data if candles not present
def Create1MinCandlesInDb(env, dbconn, date, table):

    dict = {"result": "ok", "error": "nil"}

    #  function return ticks if called on same day as
    # cdl = db.getCdlBtwnTime(env, dbconn, "", date, ["09:00", "16:00"], "1")
    # if len(cdl) > 0:
    #     dict["result"] = "fail"
    #     dict["error"] = (
    #         "Candles are present in table for " + date + ", skipping operation"
    #     )
    # return dict

    df = db.fetchTicksData(env, dbconn, date, table)
    if len(df) == 0:
        dict["result"] = "fail"
        dict["error"] = "No ticks found for " + date
        return dict

    df = libCdl.TickToCdl(df, date, "1T")

    tsDB.updateTable(dbconn, "candles_1min", df)

    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or ".")
    csvPath = script_dir + "/Data/candle_converter/"

    if table == "fut" or table == "all":

        dfFut = df[df["symbol"].str.contains("-FUT") == True]
        f = (
            csvPath
            + date
            + " ( Symbols "
            + str(len(dfFut.symbol.unique()))
            + " - Rows "
            + str(len(dfFut))
            + " ).csv"
        )

        dfFut.to_csv(f, index=True)
        dict["ticks_nsefut"] = f.replace(csvPath, "")

    if table == "stk" or table == "all":
        dfStk = df[df["symbol"].str.contains("-FUT") == False]
        f = (
            csvPath
            + date
            + " ( Symbols "
            + str(len(dfStk.symbol.unique()))
            + " - Rows "
            + str(len(dfStk))
            + " ).csv"
        )

        dfStk.to_csv(f, index=True)
        dict["ticks_nsestk"] = f.replace(csvPath, "")

    if table != "stk" or table != "fut" or table != "all":
        dict["result"] = "fail"
        dict["error"] = "invalid table selected > " + table + ", skipping operation"
    return dict
