import numpy as np
import pandas as pd


def fn_time_diff(row):

    val = np.nan
    try:
        if row["dir"] == "bearish" or row["dir"] == "bullish":
            t1 = pd.to_datetime(row["entry_time"])
            t2 = pd.to_datetime(row["exit_time"])
            val = t2 - t1
            val = val.total_seconds()
    finally:
        return val


def fn_gains(row):

    val = np.nan
    try:
        if row["dir"] == "bearish":
            val = row["entry"] - row["exit"]
        elif row["dir"] == "bullish":
            val = row["exit"] - row["entry"]
    finally:
        return val


def generate_performance_report(fin, df, fout):

    # load df from csv file
    if fin != "":
        df = pd.read_csv(fin)

    # filter candles with data
    result = df[df["status"].str.contains("signal-processed") == True]

    # -------------------------------------------------------------------------------- add missing columns/data

    result = result.fillna(0)
    if "exit_reason" not in result.columns:
        result["exit_reason"] = "data err - exit_reason missing"
        result["exit"] = result["entry"]

    if "exit_time" not in result.columns:
        result["exit_reason"] = result["exit_reason"] + "data err - exit_time missing"
        result["exit_time"] = result["entry_time"]

    # -------------------------------------------------------------------------------- gain calculations
    result["gain"] = result.apply(fn_gains, axis=1)

    # -------------------------------------------------------------------------------- counts for stats
    total_rows = len(df.index)
    err_count = result["status"].str.contains(r"ERR").sum()
    na_count = result["dir"].str.fullmatch(r"na").sum()
    bullish_count = result["dir"].str.fullmatch(r"bullish").sum()
    bearish_count = result["dir"].str.fullmatch(r"bearish").sum()
    failed_bullish_count = result["dir"].str.fullmatch(r"failed bullish").sum()
    failed_bearish_count = result["dir"].str.fullmatch(r"failed bearish").sum()

    # -------------------------------------------------------------------------------- gain calculations
    total_gain = round(result.loc[result["exit_reason"] == "target"]["gain"].sum(), 1)
    total_gain_mean = round(
        result.loc[result["exit_reason"] == "target"]["gain"].mean(), 1
    )
    total_loss = round(
        result.loc[result["exit_reason"] == "sl/deepsl"]["gain"].sum(), 1
    )
    total_loss_mean = round(
        result.loc[result["exit_reason"] == "sl/deepsl"]["gain"].mean(), 1
    )
    total_pts = round(total_gain + total_loss)

    # -------------------------------------------------------------------------------- trade type counts
    win_count = result["exit_reason"].str.fullmatch(r"target").sum()
    sl_count = result["exit_reason"].str.fullmatch(r"sl/deepsl").sum()
    eod_count = result["exit_reason"].str.fullmatch(r"eod").sum()
    total_trades_count = win_count + sl_count + eod_count

    # -------------------------------------------------------------------------------- percentages calculation
    winning_per = (win_count * 100) / total_trades_count
    winning_per = round(winning_per, 1)
    loosing_per = (sl_count * 100) / total_trades_count
    loosing_per = round(winning_per, 1)

    # -------------------------------------------------------------------------------- time delta calculation
    result["time_diff"] = result.apply(fn_time_diff, axis=1)
    win_time_avg = result.loc[result["exit_reason"] == "target"]["time_diff"].mean()
    win_time_min = result.loc[result["exit_reason"] == "target"]["time_diff"].min()
    win_time_max = result.loc[result["exit_reason"] == "target"]["time_diff"].max()
    loss_time_avg = result.loc[result["exit_reason"] == "sl/deepsl"]["time_diff"].mean()
    loss_time_min = result.loc[result["exit_reason"] == "sl/deepsl"]["time_diff"].min()
    loss_time_max = result.loc[result["exit_reason"] == "sl/deepsl"]["time_diff"].max()

    # convert seconds to minutes
    win_time_avg = round((win_time_avg / 60))
    win_time_min = round((win_time_min / 60))
    win_time_max = round((win_time_max / 60))
    loss_time_avg = round((loss_time_avg / 60))
    loss_time_min = round((loss_time_min / 60))
    loss_time_max = round((loss_time_max / 60))
    # -------------------------------------------------------------------------------- save report csv
    result.to_csv(fout + ".csv")

    # -------------------------------------------------------------------------------- generate summary report
    report_summary = {
        "new-section-info": "info",
        "strategy": result.iloc[0]["strategy"],
        "instrument": result.iloc[0]["instr"],
        "new-section-win-loss": "win-loss",  # ------------------------- section marker - win/loss
        "strike ratio": "Target : "
        + str(win_count)
        + "  Stop Loss : "
        + str(sl_count)
        + "  EoD : "
        + str(eod_count),
        "total": str(total_trades_count),
        "winning_%": str(winning_per) + "%",
        "losing_%": str(loosing_per) + "%",
        "total_points_(win+loss)": str(total_pts) + " [eod cal. missing!]",
        # "avg total point (win+loss)": str(total_pts),
        "new-section-avg": "avg",  # ----------------------------------- section marker - avg
        "win_avg": str(total_gain_mean),
        "win_total": str(total_gain),
        "loss_avg": str(total_loss_mean),
        "loss_total": str(total_loss),
        "new-section-mma": "max min avg",  # --------------------------- section marker - max/min/avg
        "win_time_(min)": "Avg:"
        + str(win_time_avg)
        + " [ min:"
        + str(win_time_min)
        + " / max:"
        + str(win_time_max)
        + " ]",
        "loss_time_(min)": "Avg:"
        + str(loss_time_avg)
        + " [ min:"
        + str(loss_time_min)
        + " / max:"
        + str(loss_time_max)
        + " ]",
        "win_drawdown": "missing data!",
        "loss_drawdown": "missing data!",
        "new-section-data": "data",  # --------------------------------- section marker - data
        "total_data": str(total_rows),
        "data_err %": str(round((err_count / total_rows) * 100, 2)),
        "new-section-stats": "stats",  # ------------------------------- section marker - stats
        "bullish": str(bullish_count),
        "bearish": str(bearish_count),
        "failed_bullish": str(failed_bullish_count),
        "failed_bearish": str(failed_bearish_count),
        "na": str(na_count),
    }

    return report_summary
