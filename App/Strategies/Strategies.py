from ast import Or
from numpy import setdiff1d
from App.Strategies.S001_ORB_F import S001_ORB
import App.DB.tsDB as db
from App.Libraries.lib_AlgoParams import AlgoParam
import App.Libraries.lib_results as res
import pandas as pd
import json


def execute(dbConn, multisymbol, algo, symbol, date):

    summary = pd.DataFrame(columns=res.trade_signal_header_list)
    results = pd.DataFrame(columns=res.trade_signal_header_list)

    # 1. Fetch params for algo
    algoParams = db.readAlgoParamsJson(dbConn, algo)
    # print(algoParams["strategy_id"])

    # 2. Fetch candles
    if (multisymbol == True):
        cdl = db.fetchCandlesBetweenMultiSymbol(dbConn, symbol,
                                                date + " 09:00",
                                                date + " 09:30", "5")
    else:
        cdl = db.fetchCandlesBetweenSingleSymbol(dbConn, symbol,
                                                 date + " 09:00",
                                                 date + " 09:30", "5")
    # print(cdl)
    sym = cdl.symbol.unique()

    # 3. Run algo for each symbol
    baseAlgo = algo[:-4]
    if baseAlgo == "S001-ORB":
        for x in range(len(sym)):
            rslt_df = cdl[cdl['symbol'] == sym[x]]
            # print(sym[x])
            rslt_df.set_index('candle', inplace=True)
            S001_ORB(algo, rslt_df, date, algoParams, results)
            # print(results)
            if (results.at[0, "dir"] == "Bullish") or \
                (results.at[0, "dir"] == "Bearish"):
                summary = summary.append(results)

        # db.saveTradeSignalsToDB(dbConn, summary)
        json_str = summary.to_json(orient="records")
        parsed = json.loads(json_str)

        return parsed
    else:
        return "No Algo Found"
