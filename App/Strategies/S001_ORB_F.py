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

from datetime import datetime
import App.Libraries.lib_FN as libFn

ENTRY_GAP_DELTA_PERCENTAGE = 0


#  algo inputs
# --------------
#  algo = "S001-ORB"
#  df - dataframe (candles size 5 min)
#  symbol = "BANKNIFTY"
#  date = "2022-01-25"
#
def S001_ORB_entr(algo, symbol, df, date, algoParams, results):

    try:

        date_time_obj = datetime.strptime(date, '%Y-%m-%d')

        # Scan date to be used for backtesting, else use current date for real trading
        if date_time_obj.date() != datetime.today().date():
            timeStamp = date + " 09:30:00"
        else:
            timeStamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        results.at[0, "strategy"] = algo
        results.at[0, "date"] = timeStamp

        results.at[0, "status"] = "signal-processed"

        # Get ORB
        orb_low, orb_high = libFn.getORB(df)
        # orb_low = df.at[date + ' 09:15:00', 'low']
        # orb_high = df.at[date + ' 09:15:00', 'high']

        cdl_926 = df.at[date + ' 09:25:00', 'close']
        cdl_926open = df.at[date + ' 09:25:00', 'open']
        cdl_930 = df.at[date + ' 09:30:00', 'close']
        results.at[0, "instr"] = symbol

        orbDelta = (abs(orb_high - orb_low) * ENTRY_GAP_DELTA_PERCENTAGE) / 100

        if cdl_930 > (orb_high + orbDelta):
            if cdl_930 > cdl_926open:  # Green candle
                results.at[0, "dir"] = "Bullish"
                calVal = cdl_930 + (
                    (cdl_930 * algoParams['controls']['target_per']) / 100)
                # results.at[0, "DeepStopLoss"] = cdl_930 * algoParams['controls']['deep_stoploss_per'] / 100
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
                    (cdl_930 * algoParams['controls']['target_per']) / 100)
                results.at[0, "stoploss"] = cdl_926open
                # results.at[0, "DeepStopLoss"] = cdl_930 * algoParams['controls']['deep_stoploss_per'] / 100
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
        results.at[0,
                   "debug"] = ("#orb_low:" + str(orb_low) + ":red-1" +
                               "#orb_high:" + str(orb_high) + ":green-1" +
                               "#cdl_926:" + str(cdl_926) + ":info-5" +
                               "#cdl_926open:" + str(cdl_926open) + ":info-5" +
                               "#cdl_930:" + str(cdl_930) + ":info-5" +
                               "#orbDelta:" + str(orbDelta) + ":data")
        return results


def S001_ORB_exit(algo, symbol, df, date, algoParams, results):
    return ""

    #   <th>strategy</th>
    #   <th>enabled</th>
    #   <th>engine</th>
    #   <th>trigger_time</th>
    #   <th>trigger_days</th>
    #   <th>cdl_size</th>
    #   <th>instruments</th>
    #   <th>controls</th>
    #   <th>percentages.target</th>
    #   <th>percentages.sl</th>
    #   <th>percentages.deepsl</th>
    #   <th>target-controls.trail_target_en</th>
    #   <th>target-controls.position_reversal_en</th>
    #   <th>target-controls.delayed_stoploss_min</th>
    #   <th>target-controls.stall_detect_period_min</th>