import json
import pandas as pd

import App.DB.tsDB as db
import App.Strategies.S001_ORB_F as S001
import App.Libraries as lib


def execute(dbConn, algoID, symbol, date, ticks, trading):

    summary = pd.DataFrame(columns=lib.lib_results.trade_signal_header_list)
    results = pd.DataFrame(columns=lib.lib_results.trade_signal_header_list)

    # 1. Fetch params for algo
    algoParams = db.readAlgoParamsJson(dbConn, algoID[0:7])

    # 2. Fetch candles
    cdl = db.getCdlBtwnTime(dbConn, symbol, date + " 09:00", date + " 09:31",
                            "1")
    if len(cdl) == 0:
        return "No candles found for " + symbol + " on " + date

    sym = cdl.symbol.unique()

    # 3. Run algo for each symbol
    baseAlgo = algoID[0:4]
    if baseAlgo == "S001":
        for x in range(len(sym)):
            rslt_df = cdl[cdl['symbol'] == sym[x]]
            # print(sym[x])
            rslt_df.set_index('time', inplace=True)
            if '-entr' in algoID:
                S001.S001_ORB_entr(algoID, symbol, rslt_df, date, algoParams,
                                   results)
            else:
                S001.S001_ORB_exit(algoID, symbol, rslt_df, date, algoParams,
                                   results)

            if trading:
                if (results.at[0, "dir"] == "Bullish") or \
                    (results.at[0, "dir"] == "Bearish"):
                    summary = summary.append(results)
            else:
                summary = summary.append(results)

        if trading:
            json_str = summary.to_json(orient="records")
            parsed = json.loads(json_str)
            return parsed  # return JSON data - API caller
        else:
            return summary  # return DF data - Researcher caller

    elif baseAlgo == "S999":
        s.S999_TEST(algo, symbol, cdl, date, algoParams, results)
        summary = summary.append(results)
        json_str = summary.to_json(orient="records")
        parsed = json.loads(json_str)
        return parsed

    else:
        return "No Algo Found"
