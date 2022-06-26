import os
import pandas as pd
from tqdm import tqdm

import App.DB.tsDB as db
import App.Strategies.Strategies as s
import App.Libraries.lib_FN as libFn
import App.Libraries.lib_BACKTEST as libBk


def backtesting(analysis_algorithm, analysis_symbol,
                analysis_duration_backward, analysis_end_date, env, dbConn,
                trading_mode, plot_images):

    start, end = libFn.getDates(analysis_duration_backward, analysis_end_date)

    scan_dates = db.get_dates_list(dbConn, start, end)

    result = pd.DataFrame(columns=None)

    print("Analysis")
    for dt in tqdm(scan_dates, colour='#23c33a'):

        df_entr = s.execute(env=env,
                            dbConn=dbConn,
                            mode="entr",
                            algoID=analysis_algorithm,
                            symbol=analysis_symbol,
                            date=dt,
                            pos_dir="",
                            pos_entr_price=0,
                            pos_entr_time="",
                            trading=trading_mode)  # get all entry calls
        df_r = df_entr

        if df_entr.at[0, 'dir'] == 'Bullish' or df_entr.at[0,
                                                           'dir'] == 'Bearish':

            df_exit = s.execute(env=env,
                                dbConn=dbConn,
                                mode="exit",
                                algoID=analysis_algorithm,
                                symbol=analysis_symbol,
                                date=dt,
                                pos_dir=df_entr.at[0, 'dir'],
                                pos_entr_price=df_entr.at[0, 'entry'],
                                pos_entr_time=df_entr.at[0, 'date'],
                                trading=trading_mode)  # get all exit calls

            df_r.at[0, "exit"] = df_exit.at[0, "exit"]
            df_r.at[0, "exit_time"] = df_exit.at[0, "exit_time"]
            df_r.at[0, "exit_reason"] = df_exit.at[0, "exit_reason"]

        result = result.append(df_r)

    libBk.btResultsParser(
        env=env,
        dbConn=dbConn,
        scan_dates=scan_dates,
        result=result,
        plot_images=plot_images,
        analysis_algorithm=analysis_algorithm,
        analysis_symbol=analysis_symbol,
        analysis_duration_backward=analysis_duration_backward)
