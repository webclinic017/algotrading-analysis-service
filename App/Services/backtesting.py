import os
import pandas as pd
from tqdm import tqdm
import json

import App.DB.tsDB as db
import App.Strategies.Strategies as s
import App.Libraries.lib_fn as libFn
import App.Libraries.lib_BACKTEST as libBk


def backtesting(
    analysis_algorithm,
    analysis_symbol,
    analysis_duration_backward,
    analysis_end_date,
    env,
    dbConn,
    trading_mode,
    plot_images,
):

    start, end = libFn.getDates(analysis_duration_backward, analysis_end_date)

    scan_dates = db.get_dates_list(dbConn, start, end)

    result = pd.DataFrame(columns=None)

    print("Analysis")
    for dt in tqdm(scan_dates, colour="#23c33a"):

        df_entr = s.execute(
            env=env,
            dbConn=dbConn,
            mode="entr",
            algoID=analysis_algorithm,
            symbol=analysis_symbol,
            date=dt,
            pos_dir="",
            pos_entr_price=0,
            pos_entr_time="",
            trading=trading_mode,
        )  # get all entry calls
        df_r = df_entr
        if len(df_entr) > 1:
            print(
                "Fatal error - Expected 1 result form signal analysis, actual ",
                len(df_entr),
            )
            return
        # print(df_entr)
        if df_entr.at[0, "dir"] == "bullish" or df_entr.at[0, "dir"] == "bearish":

            df_exit = s.execute(
                env=env,
                dbConn=dbConn,
                mode="exit",
                algoID=analysis_algorithm,
                symbol=analysis_symbol,
                date=dt,
                pos_dir=df_entr.at[0, "dir"],
                pos_entr_price=df_entr.at[0, "entry"],
                pos_entr_time=df_entr.at[0, "entry_time"],
                trading=trading_mode,
            )  # get all exit calls

            df_r.at[0, "exit"] = df_exit.at[0, "exit"]
            df_r.at[0, "exit_time"] = df_exit.at[0, "exit_time"]
            df_r.at[0, "exit_reason"] = df_exit.at[0, "exit_reason"]
            df_r.at[0, "status"] = df_exit.at[0, "status"]

            # merge debug informations
            dbg_entr = json.loads(df_r.iloc[0]["debug_entr"])
            dbg_exit = json.loads(df_exit.iloc[0]["debug_exit"])
            dbg_info = dbg_entr + dbg_exit
            json_object = json.dumps(dbg_info)
            df_r.at[0, "debug"] = json_object

        result = result.append(df_r)

    libBk.btResultsParser(
        env=env,
        dbConn=dbConn,
        result=result,
        plot_images=plot_images,
        analysis_algorithm=analysis_algorithm,
        analysis_symbol=analysis_symbol,
        analysis_duration_backward=analysis_duration_backward,
    )
