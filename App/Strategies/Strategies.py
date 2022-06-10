import json
import pandas as pd

import App.DB.tsDB as db
import App.Strategies.S001_ORB_F as S001
import App.Libraries.lib_STRUCTS as libr


def execute(env, dbConn, algoID, symbol, date, trading):

    summary = pd.DataFrame(columns=libr.trade_signal_hl)
    results = pd.DataFrame(columns=libr.trade_signal_hl)
    # results = pd.DataFrame(columns=None)

    # 1. Fetch params for algo
    algoParams = db.readAlgoParams(env, dbConn, algoID[0:7])
    if algoParams == None:
        summary.at[0, "status"] = "ERR: No algoParams found for " + algoID[
            0:7] + " on " + date
        return returnValues(summary, trading)

    # 2. Fetch candles
    cdl = db.getCdlBtwnTime(env, dbConn, symbol, date, ["09:00", "09:31"], "1")
    if len(cdl) == 0:
        summary.at[
            0,
            "status"] = "ERR: No candles found for " + symbol + " on " + date
        return returnValues(summary, trading)

    sym = cdl.symbol.unique()

    # 3. Run algo for each symbol
    baseAlgo = algoID[0:4]
    if baseAlgo == "S001":
        for x in range(len(sym)):
            rslt_df = cdl[cdl['symbol'] == sym[x]]
            # rslt_df.set_index('time', inplace=True)
            if '-entr' in algoID:
                S001.S001_ORB_entr(algoID, symbol, rslt_df, date, algoParams,
                                   results)
            else:
                S001.S001_ORB_exit(algoID, symbol, rslt_df, date, algoParams,
                                   results)
            summary = summary.append(results)

        return returnValues(summary, trading)

    elif baseAlgo == "S999":
        s.S999_TEST(algo, symbol, cdl, date, algoParams, results)
        summary = summary.append(results)
        json_str = summary.to_json(orient="records")
        parsed = json.loads(json_str)
        return parsed

    else:
        return "No Algo Found"


def returnValues(summary, trading):
    if trading:
        json_str = summary.to_json(orient="records")
        parsed = json.loads(json_str)
        return parsed  # return JSON data - API caller
    else:
        return summary  # return DF data - Researcher caller
