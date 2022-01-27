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

import pandas as pd

# from lib_ORB import getORB
# from lib_CANDLES import getTimeCandle
# from lib_ENCODE import encodeExitCriteria

import App.Libraries.lib_ORB as orb
import App.Libraries.lib_CANDLES as c
from App.Libraries.lib_AlgoParams import AlgoParam

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

        results.at[0, "Strategy"] = algo
        results.at[0, "Date"] = date

        # orb_low, orb_high = orb.getORB(df)
        orb_low = df.at[date + ' 09:15', 'low'][0]
        orb_high = df.at[date + ' 09:15', 'high'][0]

        cdl_926 = df.at[date + ' 09:25', 'close'][0]
        cdl_926open = df.at[date + ' 09:25', 'open'][0]
        cdl_930 = df.at[date + ' 09:30', 'close'][0]

        orbDelta = (abs(orb_high - orb_low) * ENTRY_GAP_DELTA_PERCENTAGE) / 100

        if cdl_930 > (orb_high + orbDelta):
            if cdl_930 > cdl_926open:  # Green candle
                results.at[0, "Signal"] = "Bullish"
                results.at[0, "Target"] = cdl_930 + (
                    cdl_930 * algoParams[AlgoParam.target_per.value] / 100)

                results.at[0, "DeepStopLoss"] = cdl_930 * algoParams[
                    AlgoParam.deep_stoploss_per.value] / 100

                results.at[0, "StopLoss"] = cdl_926open
                results.at[0, "Entry"] = cdl_930
                results.at[0, "EntryTime"] = "09:30"
            else:
                results.at[0, "Signal"] = "Failed Bullish"

        elif cdl_930 < (orb_low - orbDelta):
            if cdl_930 < cdl_926open:  # Red candle
                results.at[0, "Signal"] = "Bearish"
                results.at[0, "Target"] = cdl_930 - (
                    cdl_930 * algoParams[AlgoParam.target_per.value] / 100)
                results.at[0, "StopLoss"] = cdl_926open
                results.at[0, "DeepStopLoss"] = cdl_930 * algoParams[
                    AlgoParam.deep_stoploss_per.value] / 100
                results.at[0, "Entry"] = cdl_930
                results.at[0, "EntryTime"] = "09:30"
            else:
                results.at[0, "Signal"] = "Failed Bearish"

        else:
            results.at[0, "Signal"] = "NA"

    except Exception as e:
        # print("Data Error", date)
        print(e)
        results.at[0, "Signal"] = "Data Error"
        return results

    else:
        return results
