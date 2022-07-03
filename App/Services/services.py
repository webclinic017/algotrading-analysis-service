from numpy import double
from App.Services.create_candles import Create1MinCandlesInDb
from App.Services.instruments import LoadInstruments
import pandas as pd
import json


def execute(env, dbConn, sid, date):

    if sid == "instruments":
        results = LoadInstruments(env, dbConn)
    elif sid == "create_candles_day":
        result = Create1MinCandlesInDb(env, dbConn, date)
        d = json.dumps(result, indent=4)
        p = json.loads(d)
        return p  # return JSON data - API caller
    else:
        return "No Service Found"
