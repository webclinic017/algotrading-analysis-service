# Strategy - ORB - May the force be with you!
# ---------------------------ENTRY--------------------------------
# Candle Size - 5 Min
# 9:26-9:30, this 5min candle shall be green for bullish and red for bearish
# 9:30am candle close shall be beyond 5% of ORB Delta than ORB High/Low respectively
# ----------------------------EXIT--------------------------------
# SL shall be 9:26 min candle open
# Exit - Target/Stall Detection/Direction Reversals/3:30 EoD
# DeepSL - 150 pts open postioin SL - To Be Evaluated
# ----------------------------SUBs--------------------------------
# Subscription services - Stall/Direction from position
# ----------------------------------------------------------------
import datetime
from dateutil import parser
from pytz import timezone
from tzlocal import get_localzone


def S999_TEST(algo, symbol, df, date, algoParams, results):

    import pytz, datetime

    latz = pytz.timezone("Asia/Kolkata")

    dt = datetime.datetime.now(get_localzone())
    dt2 = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                            dt.second, 0, latz)
    timeStamp = dt2.isoformat()

    results.at[0, "strategy"] = algo
    results.at[0, "date"] = timeStamp
    results.at[0, "instr"] = symbol
    results.at[0, "dir"] = "Bullish"
    results.at[0, "target"] = 100
    results.at[0, "stoploss"] = 200
    results.at[0, "entry"] = 300
    results.at[0, "entry_time"] = timeStamp
