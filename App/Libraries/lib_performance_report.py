import pandas as pd


def generate_performance_report(fin, df, fout):

    if fin != "":
        df = pd.read_csv(fin)

    result = df[df["status"].str.contains("signal-processed") == True]

    total_rows = len(df.index)
    err = df["status"].str.contains(r'ERR').sum()
    na = df["dir"].str.fullmatch(r'NA').sum(),
    bullish = df["dir"].str.fullmatch(r'Bullish').sum(),
    bearish = df["dir"].str.fullmatch(r'Bearish').sum(),
    failed_bullish = df["dir"].str.fullmatch(r'Failed Bullish').sum(),
    failed_bearish = df["dir"].str.fullmatch(r'Failed Bearish').sum(),

    report_summary = {
        "new-section-info": 'info',
        "strategy": result.iloc[0]["strategy"],
        "instrument": result.iloc[0]["instr"],
        "new-section-winlose": 'winlose',
        "winning": str(0),
        "winning_%": str(0),
        "losing": str(0),
        "losing_%": str(0),
        "new-section-avg": 'avg',
        "avg_win": str(0),
        "avg_win_%": str(0),
        "avg_loss": str(0),
        "avg_loss_%": str(0),
        "avg_time": str(0),
        "avg_time_%": str(0),
        "avg_time_(max)": str(0),
        "avg_time_(min)": str(0),
        "new-section-drawdown": 'drawdown',
        "drawdown_(max)": str(0),
        "drawdown_%_(max)": str(0),
        "drawdown_(min)": str(0),
        "drawdown_%_(min)": str(0),
        "drawdown_(avg)": str(0),
        "drawdown_%_(avg)": str(0),
        "new-section-data": 'data',
        "total_data": str(total_rows),
        "data_err %": str(round((err / total_rows) * 100, 2)),
        "new-section-stats": 'stats',
        "bullish": str(bullish[0]),
        "bearish": str(bearish[0]),
        "failed_bullish": str(failed_bullish[0]),
        "failed_bearish": str(failed_bearish[0]),
        "na": str(na[0]),
        "none": "none",
    }

    return report_summary
