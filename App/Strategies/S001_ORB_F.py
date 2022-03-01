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

from sqlite3 import Timestamp
import pandas as pd
import datetime
from dateutil import parser
from pytz import timezone
from tzlocal import get_localzone

# from lib_ORB import getORB
# from lib_CANDLES import getTimeCandle
# from lib_ENCODE import encodeExitCriteria

import App.Libraries.lib_ORB as orb
import App.Libraries.lib_CANDLES as c

ENTRY_GAP_DELTA_PERCENTAGE = 0


#  algo inputs
# --------------
#  algo = "S001-ORB"
#  df - dataframe (candles size 5 min)
#  symbol = "BANKNIFTY"
#  date = "2022-01-25"
#
def S001_ORB(algo, df, date, algoParams, results):

    try:

        # Convert to local time zone

        # d = "2019-12-25T23:59:59+00:00"
        # print(datetime.strptime(d, "%Y-%m-%dT%H:%M:%S%z"))

        import pytz, datetime

        latz = pytz.timezone("Asia/Kolkata")
        print(latz)

        dt = datetime.datetime.now(get_localzone())
        dt2 = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
                                dt.second, 0, latz)
        timeStamp = dt2.isoformat()

        # ct = datetime.datetime.now()
        # now_local = ct.astimezone(get_localzone())
        # timeStamp = now_local.strftime("%Y-%m-%dT%H:%M:%S%z")
        # timeStamp = ct.isoformat()
        # x = parser.parse(timeStamp)
        # timeStamp = "2022-02-27T18:00:32+05:30"  -- working format (required for golang parsing)

        results.at[0, "strategy"] = algo
        results.at[0, "date"] = timeStamp

        # orb_low, orb_high = orb.getORB(df)
        # print(df.at[date + ' 09:15', 'low'])
        orb_low = df.at[date + ' 09:15', 'low']
        orb_high = df.at[date + ' 09:15', 'high']

        cdl_926 = df.at[date + ' 09:25', 'close']
        cdl_926open = df.at[date + ' 09:25', 'open']
        cdl_930 = df.at[date + ' 09:30', 'close']
        results.at[0, "instr"] = df.at[date + ' 09:15', 'symbol']

        orbDelta = (abs(orb_high - orb_low) * ENTRY_GAP_DELTA_PERCENTAGE) / 100

        if cdl_930 > (orb_high + orbDelta):
            if cdl_930 > cdl_926open:  # Green candle
                results.at[0, "dir"] = "Bullish"
                calVal = cdl_930 + (
                    (cdl_930 * algoParams["p_target_per"][0]) / 100)
                # results.at[0, "DeepStopLoss"] = cdl_930 * algoParams["p_deep_stoploss_per"] / 100
                results.at[0, "target"] = calVal
                results.at[0, "stoploss"] = cdl_926open
                results.at[0, "entry"] = cdl_930
                results.at[0, "entry_time"] = timeStamp
            else:
                results.at[0, "dir"] = "Failed Bullish"

        elif cdl_930 < (orb_low - orbDelta):
            if cdl_930 < cdl_926open:  # Red candle
                results.at[0, "dir"] = "Bearish"
                results.at[0, "target"] = cdl_930 - (
                    (cdl_930 * algoParams["p_target_per"][0]) / 100)
                results.at[0, "stoploss"] = cdl_926open
                # results.at[0, "DeepStopLoss"] = cdl_930 * algoParams["p_deep_stoploss_per"] / 100
                results.at[0, "entry"] = cdl_930
                results.at[0, "entry_time"] = timeStamp
            else:
                results.at[0, "dir"] = "Failed Bearish"

        else:
            results.at[0, "dir"] = "NA"

    except Exception as e:
        # print("Data Error", date)
        print(e)
        results.at[0, "dir"] = "Data Error"
        return results

    else:
        return results
