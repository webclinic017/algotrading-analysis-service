import pandas as pd
import App.DB.tsDB as db
import App.Services.backtesting as bt


def research():
    SIMULATION = False
    env = db.envVar()
    dbConn = db.dbConnect(env)

    analysis_algorithm = "S001-01-ORB-OpeningRangeBreakout"
    analysis_symbol = "BANKNIFTY-FUT"
    analysis_duration_backward = "5 months"
    analysis_end_date = "2022-06-01"  # "" for today

    bt.backtesting(analysis_algorithm=analysis_algorithm,
                   analysis_symbol=analysis_symbol,
                   analysis_duration_backward=analysis_duration_backward,
                   analysis_end_date=analysis_end_date,
                   dbConn=dbConn,
                   env=env,
                   trading_mode=SIMULATION,
                   plot_images=False)


import App.Libraries.lib_performance_report as pr

print(
    pr.generate_performance_report(
        fin=
        "/config/workspace/algotrading-analysis-service/StudyZone/results/318796-2022-06-29__3:04PM-BANKNIFTY-FUT-5months.csv",
        df=pd.DataFrame(),
        fout="test-out"))

# research()
