from numpy import setdiff1d
from App.Strategies.S001_ORB_F import S001_ORB
import App.DB.tsDB as db
from App.Libraries.lib_AlgoParams import AlgoParam
import pandas as pd


def execute(dbConn, algo):

    results = pd.DataFrame()

    # 1. Fetch params for algo
    algoParams = db.readAlgoParams(dbConn, algo)
    # print(algoParams[AlgoParam.strategy_id.value])

    # 2. Fetch candles
    selDate = '2022-01-08'
    cdl = db.fetchCandlesOnDate(dbConn, '', selDate, "1")
    print(cdl)

    # cdl = db.fetchCandlesOnDate(dbConn, 'TEST_Signal', "2022-01-08", "1")

    # cdl = db.fetchCandlesBetweenTime(dbConn, 'TEST_Signal', "2022-01-08 23:00", "2022-01-08 23:04", "1")

    # 3. Run algo

    baseAlgo = algo[:-4]
    if baseAlgo == "S001-ORB":
        results = S001_ORB(algo, cdl, selDate, algoParams, results)
        return results
    else:
        return "No Algo Found"
