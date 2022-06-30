import json
import pandas as pd

import App.DB.tsDB as db
from App.Strategies import *
import App.Libraries.lib_STRUCTS as libr


def execute(env, dbConn, mode, algoID, symbol, date, pos_dir, pos_entr_price,
            pos_entr_time, trading):

    summary = pd.DataFrame(columns=libr.trade_signal_hl)
    results = pd.DataFrame(columns=libr.trade_signal_hl)
    # results = pd.DataFrame(columns=None)

    # 1. Fetch params for algo
    algoParams = db.readAlgoParams(env, dbConn, algoID[0:7])
    if algoParams == None:
        summary.at[0, "status"] = "ERR: No algoParams found for " + algoID[
            0:7] + " on " + date
        return returnValues(summary, trading)

    # 2. Fetch candles as per algoParams interval defined for the day
    cdl = db.getCdlBtwnTime(env, dbConn, symbol, date, ["09:00", "16:00"], "1")
    if len(cdl) == 0:
        summary.at[
            0,
            "status"] = "ERR: No candles found for " + symbol + " on " + date
        return returnValues(summary, trading)

    # 3. Run algo for each symbol
    baseAlgo = algoID[0:4].lower()

    sym = cdl.symbol.unique()
    for x in range(len(sym)):
        rslt_df = cdl[cdl['symbol'] == sym[x]]

        if baseAlgo == "s001":

            S001_ORB_F.S001_ORB(algoID, mode, symbol, rslt_df, date,
                                algoParams, pos_dir, pos_entr_price,
                                pos_entr_time, results)

        elif baseAlgo == "s002":
            s002_orb_immediate_crossover.analysis(algoID, mode, symbol,
                                                  rslt_df, date, algoParams,
                                                  pos_dir, pos_entr_price,
                                                  pos_entr_time, results)

        elif baseAlgo == "s999":
            S999_TEST_F.return_success_test(algoID, symbol, cdl, date,
                                            algoParams, results)

        else:
            return "No Algo Found"

        summary = summary.append(results)

    return returnValues(summary, trading)


def returnValues(summary, trading):
    if trading:
        json_str = summary.to_json(orient="records")
        parsed = json.loads(json_str)
        return parsed  # return JSON data - API caller
    else:
        return summary  # return DF data - Researcher caller
