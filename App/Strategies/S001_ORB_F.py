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

from datetime import datetime, timedelta

import App.Libraries.lib_FN as libFn
import App.Libraries.lib_CANDLES as libCdl

ENTRY_GAP_DELTA_PERCENTAGE = 0

#  algo inputs
# --------------
#  algo = "S001-ORB"
#  df - dataframe (candles size 5 min)
#  symbol = "BANKNIFTY"
#  date = "2022-01-25"
#


def S001_ORB(algoID, mode, symbol, df, date, algoParams, pos_dir,
             pos_entr_price, pos_entr_time, results):

    if mode == "entr":
        S001_ORB_entr(algoID, symbol, df, date, algoParams, results)
    elif mode == "exit":
        S001_ORB_exit(algoID, symbol, df, date, algoParams, pos_dir,
                      pos_entr_price, pos_entr_time, results)
    else:
        results.at[0, "status"] = "ERR: Invalid mode " + mode

    return results


def S001_ORB_entr(algoID, symbol, df, date, algoParams, results):

    try:

        date_time_obj = datetime.strptime(date, "%Y-%m-%d")

        # Scan date to be used for backtesting, else use current date for real trading
        if date_time_obj.date() != datetime.today().date():
            timeStamp = date + " 09:30:00"
        else:
            timeStamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        results.at[0, "strategy"] = algoID
        results.at[0, "date"] = timeStamp

        results.at[0, "status"] = "signal-processed"

        # Get ORB
        # orb_low, orb_high = libFn.getORB(df)
        orb_low = df.at[date + " 09:15:00", "low"]
        orb_high = df.at[date + " 09:15:00", "high"]

        cdl_926 = df.at[date + " 09:25:00", "close"]
        cdl_926open = df.at[date + " 09:25:00", "open"]
        cdl_930 = df.at[date + " 09:30:00", "close"]
        results.at[0, "instr"] = symbol

        orbDelta = (abs(orb_high - orb_low) * ENTRY_GAP_DELTA_PERCENTAGE) / 100

        if cdl_930 > (orb_high + orbDelta):
            if cdl_930 > cdl_926open:  # Green candle
                results.at[0, "dir"] = "Bullish"
                calVal = cdl_930 + (
                    (cdl_930 * algoParams["controls"]["target_per"]) / 100)
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
                    (cdl_930 * algoParams["controls"]["target_per"]) / 100)
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


def S001_ORB_exit(algoID, symbol, df, date, algoParams, pos_dir,
                  pos_entr_price, pos_entr_time, results):

    pPositionReversal = algoParams["controls"]["position_reversal_en"]
    pTgtTrail = algoParams["controls"]["target_trail_per"]
    pSlTrail = algoParams["controls"]["stoploss_trail_per"]
    s001_sentiment_analyser(df, pos_entr_time, pos_entr_price)

    # -------------------------------- sl & target --------------------------------
    sl = (algoParams["controls"]["stoploss_per"] / 100) * pos_entr_price
    target = (algoParams["controls"]["target_per"] / 100) * pos_entr_price

    # -------------------------------- filter cdl --------------------------------
    dly_sl = algoParams["controls"]["delayed_stoploss_seconds"]
    posentr = datetime.strptime(pos_entr_time, "%Y-%m-%d %H:%M:%S")

    if dly_sl != 0:
        start_time = posentr + timedelta(seconds=dly_sl)
        end_time = start_time.replace(hour=15, minute=31, second=0)
    else:
        start_time = pos_entr_time
        end_time = start_time.replace(hour=15, minute=31, second=0)

    active_cdls = libCdl.get_active_cdl(
        df, start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time.strftime("%Y-%m-%d %H:%M:%S"))

    if pos_dir.lower() == "bullish":

        for index, row in df.iterrows():

            # trail_target_mper
            # trail_sl_mper

            if row['close'] > (pos_entr_price + (pos_entr_price * pTgtTrail)):
                target = row['close'] + 
                
                sl = row['close'] - (row['close'] * pSlTrail)
                # cal new sl and target trail values

            if row['close'] > pos_entr_price + target:  # target hit
                results.at[0, "exit_time"] = index
                results.at[0, "exit"] = row['close']
                results.at[0, "exit_reason"] = "target"
                results.at[0, "status"] = "signal-processed"
                return results
            elif row['close'] < (pos_entr_price - sl):  # stoploss hit
                results.at[0, "exit_time"] = index
                results.at[0, "exit"] = row['close']
                results.at[0, "exit_reason"] = "sl/deepsl"
                results.at[0, "status"] = "signal-processed"
                return results

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Bullish
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # "delayed_stoploss_min": "2018-09-22T23:23:23Z",
        # "stall_detect_period_min": "2018-09-22T22:22:22Z",
        # "trail_target_en": true,
        # "position_reversal_en": true,
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Check for Target acheived
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        pTargetTrail = strategy.at[0, 'TrailTarget']

        Tgtmask = cdlDF['Close'] > (strategy.at[0, 'Target'])
        tgtDF = cdlDF.loc[Tgtmask]
        if (len(tgtDF) > 0):
            idx = tgtDF.index[0]
            strategy.at[0, 'Exit'] = cdlDF.at[idx, 'Close']
            strategy.at[0, 'ExitTime'] = idx.time().strftime("%H:%M")
            strategy.at[0, 'Reason'] = 'Target'

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Bearish
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if pos_dir.lower() == "bearish":
        tgt_df = df['close'] > pos_entr_price - target
        sl_df = df['close'] > (pos_entr_price + sl)
        #print('bearish')
        #if len(slDF) > 0 :
        #strategy.at[0, 'Position Exit'] == slDF.at[1, 'Close']
        #strategy.at[0, 'Position Exit time'] == slDF.at[0, index]
        #   print(slDF)

        #print(slDF)

        #print('no exits trigerred, check EoD candle')
        #print('exit', strategy.at[0, 'Exit'])
        #type(strategy.at[0, 'Exit'])

        results.at[0,
                   'Result'] = results.at[0, 'Exit'] - results.at[0, 'Entry']

    return results


def s001_sentiment_analyser(df, pos_entr_time, pos_entr_price):

    # stall detect period
    # position reversal period

    #print(period)
    # 1. count green/red candles. > 50% gives direction
    # 2. size of green/red determines the force in the direction
    # 3. Return interpreted status

    return 0
