from ast import Or
from numpy import setdiff1d
from App.Strategies.S001_ORB_F import S001_ORB
from App.Strategies.S999_TEST_F import S999_TEST
import App.DB.tsDB as db
from App.Libraries.lib_AlgoParams import AlgoParam
import App.Libraries.lib_results as res
import pandas as pd
import json


def execute(dbConn, multisymbol, algo, symbol, date):

    summary = pd.DataFrame(columns=res.trade_signal_header_list)
    results = pd.DataFrame(columns=res.trade_signal_header_list)

    # 1. Fetch params for algo
    algo = algo[:-5]
    algoParams = db.readAlgoParamsJson(dbConn, algo)

    # 2. Fetch candles
    if (multisymbol == True):
        cdl = db.fetchCandlesBetweenMultiSymbol(dbConn, symbol,
                                                date + " 09:00",
                                                date + " 09:30", "1")
    else:
        cdl = db.fetchCandlesBetweenSingleSymbol(dbConn, symbol,
                                                 date + " 09:00",
                                                 date + " 09:30", "1")
    # print(cdl)
    sym = cdl.symbol.unique()

    # 3. Run algo for each symbol
    baseAlgo = algo[:-4]
    if baseAlgo == "S001-ORB":
        for x in range(len(sym)):
            rslt_df = cdl[cdl['symbol'] == sym[x]]
            # print(sym[x])
            rslt_df.set_index('candle', inplace=True)
            S001_ORB(algo, symbol, rslt_df, date, algoParams, results)
            # print(results)
            if (results.at[0, "dir"] == "Bullish") or \
                (results.at[0, "dir"] == "Bearish"):
                summary = summary.append(results)

        # db.saveTradeSignalsToDB(dbConn, summary)
        json_str = summary.to_json(orient="records")
        parsed = json.loads(json_str)
        return parsed
    elif baseAlgo == "S999-TEST":
        S999_TEST(algo, symbol, cdl, date, algoParams, results)
        summary = summary.append(results)
        json_str = summary.to_json(orient="records")
        parsed = json.loads(json_str)
        return parsed

    else:
        return "No Algo Found"
