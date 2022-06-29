import numpy as np
import pandas as pd


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

    if fin != "":
        df = pd.read_csv(fin)

    result = df[df["status"].str.contains("signal-processed") == True]
    result = result.fillna(0)

    # result.to_csv("test.csv")
    result.to_csv(fout + ".csv")

    if "exit_reason" not in result.columns:
        result["exit_reason"] = "data err - col missing"
        result["exit"] = result["entry"]

    # create new column 'Good' using the function above
    result["gain"] = result.apply(fn_gains, axis=1)

    total_rows = len(df.index)
    err_count = result["status"].str.contains(r"ERR").sum()
    na_count = result["dir"].str.fullmatch(r"na").sum()
    bullish_count = result["dir"].str.fullmatch(r"bullish").sum()
    bearish_count = result["dir"].str.fullmatch(r"bearish").sum()
    failed_bullish_count = result["dir"].str.fullmatch(r"failed bullish").sum()
    failed_bearish_count = result["dir"].str.fullmatch(r"failed bearish").sum()
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
    total_pts = total_gain + total_loss

    win_count = result["exit_reason"].str.fullmatch(r"target").sum()
    sl_count = result["exit_reason"].str.fullmatch(r"sl/deepsl").sum()
    eod_count = result["exit_reason"].str.fullmatch(r"eod").sum()
    total_trades_count = win_count + sl_count + eod_count

    report_summary = {
        "new-section-info": "info",
        "strategy": result.iloc[0]["strategy"],
        "instrument": result.iloc[0]["instr"],
        "new-section-win-loss": "win-loss",
        "strike ratio": "Target : "
        + str(win_count)
        + "  Stop Loss : "
        + str(sl_count)
        + "  EoD : "
        + str(eod_count),
        "total": str(total_trades_count),
        "winning_%": str(round((win_count * 100 / total_trades_count), 0)) + "%",
        "losing_%": str(round((sl_count * 100 / total_trades_count), 0)) + "%",
        "total_points_(win+loss)": str(total_pts),
        # "avg total point (win+loss)": str(total_pts),
        "new-section-avg": "avg",
        "win_avg": str(total_gain_mean),
        "win_total": str(total_gain),
        "loss_avg": str(total_loss_mean),
        "loss_total": str(total_loss),
        "new-section-mma": "max min avg",
        "time_avg": str(0),
        "drawdown_avg": str(0),
        "time_min": str(0),
        "drawdown_min": str(0),
        "time_max": str(0),
        "drawdown_max": str(0),
        "new-section-data": "data",
        "total_data": str(total_rows),
        "data_err %": str(round((err_count / total_rows) * 100, 2)),
        "new-section-stats": "stats",
        "bullish": str(bullish_count),
        "bearish": str(bearish_count),
        "failed_bullish": str(failed_bullish_count),
        "failed_bearish": str(failed_bearish_count),
        "na": str(na_count),
    }

    return report_summary
