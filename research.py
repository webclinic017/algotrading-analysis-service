import App.DB.tsDB as db
import App.Services.backtesting as bt


def research():
    SIMULATION = False
    env = db.envVar()
    dbConn = db.dbConnect(env)

    analysis_algorithm = "S001-01-ORB-OpeningRangeBreakout"
    analysis_symbol = "BANKNIFTY-FUT"
    analysis_duration_backward = "6 weeks"
    analysis_end_date = ""  # "" for today

    bt.backtesting(analysis_algorithm=analysis_algorithm,
                   analysis_symbol=analysis_symbol,
                   analysis_duration_backward=analysis_duration_backward,
                   analysis_end_date=analysis_end_date,
                   dbConn=dbConn,
                   env=env,
                   trading_mode=SIMULATION,
                   plot_images=True)


research()
