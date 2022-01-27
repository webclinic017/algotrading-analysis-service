from numpy import setdiff1d
from App.Strategies.S001_ORB_F import S001_ORB
import App.DB.tsDB as db
from App.Libraries.lib_AlgoParams import AlgoParam
import pandas as pd


def execute(dbConn, algo, symbol, date):

    results = pd.DataFrame()

    # 1. Fetch params for algo
    algoParams = db.readAlgoParams(dbConn, algo)
    # print(algoParams[AlgoParam.strategy_id.value])

    # 2. Fetch candles
    cdl = db.fetchCandlesOnDate(dbConn, symbol, date, "5")
    cdl.set_index('candle', inplace=True)
    print(cdl)

    # cdl = db.fetchCandlesOnDate(dbConn, 'TEST_Signal', "2022-01-08", "1")

    # cdl = db.fetchCandlesBetweenTime(dbConn, 'TEST_Signal', "2022-01-08 23:00", "2022-01-08 23:04", "1")

    # 3. Run algo

    baseAlgo = algo[:-4]
    if baseAlgo == "S001-ORB":
        results = S001_ORB(algo, cdl, date, algoParams, results)
        print(results)
        return results.to_json(orient="index")
    else:
        return "No Algo Found"
