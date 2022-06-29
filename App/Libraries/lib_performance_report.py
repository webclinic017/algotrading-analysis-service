import numpy as np
import pandas as pd


def fn_gains(row):

    val = np.nan

    if row["dir"] == "bearish":
        val = row["entry"] - row["exit"]
    elif row["dir"] == "bullish":
        val = row["exit"] - row["entry"]

    return val


def generate_performance_report(fin, df, fout):

    if fin != "":
        df = pd.read_csv(fin)

    result = df[df["status"].str.contains("signal-processed") == True]
    result = result.fillna(0)

    # create new column 'Good' using the function above
    result["gain"] = result.apply(fn_gains, axis=1)

    result.to_csv(fout + ".csv")

    total_rows = len(df.index)
    err = result["status"].str.contains(r"ERR").sum()
    na = result["dir"].str.fullmatch(r"na").sum()
    bullish = result["dir"].str.fullmatch(r"bullish").sum()
    bearish = result["dir"].str.fullmatch(r"bearish").sum()
    failed_bullish = result["dir"].str.fullmatch(r"failed bullish").sum()
    failed_bearish = result["dir"].str.fullmatch(r"failed bearish").sum()
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
    # total_gain_mean = round(df["gain"].mean(), 2)

    win = result["exit_reason"].str.fullmatch(r"target").sum()

    target_sum = result["exit_reason"].str.fullmatch(r"target").sum()
    sl_sum = result["exit_reason"].str.fullmatch(r"sl/deepsl").sum()
    total_trades = target_sum + sl_sum

    report_summary = {
        "new-section-info": "info",
        "strategy": result.iloc[0]["strategy"],
        "instrument": result.iloc[0]["instr"],
        "new-section-winlose": "winlose",
        "strike ratio": "Target : " + str(target_sum) + "  Stop Loss : " + str(sl_sum),
        "total": str(total_trades),
        "winning_%": str(round((target_sum * 100 / total_trades), 0)) + "%",
        "losing_%": str(round((sl_sum * 100 / total_trades), 0)) + "%",
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
        "data_err %": str(round((err / total_rows) * 100, 2)),
        # "new-section-stats":
        # 'stats',
        # "bullish":
        # str(bullish[0]),
        # "bearish":
        # str(bearish[0]),
        # "failed_bullish":
        # str(failed_bullish[0]),
        # "failed_bearish":
        # str(failed_bearish[0]),
        # "na":
        # str(na[0]),
        # "none":
        # "none",
    }

    return report_summary
