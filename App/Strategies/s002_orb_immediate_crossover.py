# Strategy Name -
# ---------------------------ENTRY--------------------------------
# Candle Size -  Min
#
#
# ----------------------------EXIT--------------------------------
# SL     -
# Exit   -
# DeepSL -
# ----------------------------SUBs--------------------------------
# Subscription -
# -------------------------ALGO PARAMS----------------------------
# var 1 -
# ----------------------------------------------------------------

import json
from datetime import datetime, timedelta

import App.Libraries.lib_CANDLES as libCdl
from App.Libraries import *


def analysis(
    algoID,
    mode,
    symbol,
    df,
    date,
    algoParams,
    pos_dir,
    pos_entr_price,
    pos_entr_time,
    results,
):

    if mode == "entr":
        _entr(algoID, symbol, df, date, algoParams, results)
    elif mode == "exit":
        _exit(
            algoID,
            symbol,
            df,
            date,
            algoParams,
            pos_dir,
            pos_entr_price,
            pos_entr_time,
            results,
        )
    else:
        results.at[0, "status"] = "ERR: Invalid mode " + mode

    return results


def _entr(algoID, symbol, df, date, algoParams, results):

    d = []

    # --------------------------------------------------------------
    # Minimum data to be returned - status,date,instr,strategy,dir |
    # --------------------------------------------------------------
    results.at[0, "instr"] = symbol
    results.at[0, "strategy"] = algoID
    results.at[0, "date"] = trade_date(date)
    results.at[0, "status"] = "pending"
    results.at[0, "dir"] = "NA"
    results.at[0, "debug_entr"] = "{}"
    # -------------------------------------------------------------

    # --------------------------------------------------------------
    # Strategy                                                    |
    # --------------------------------------------------------------

    try:

        orb = df.between_time("9:15", "9:30")
        # print(check)

        # Get ORB
        orb_low = orb["low"].min()
        orb_high = orb["high"].max()

        data = df.between_time("9:30", "15:15")
        c = list(data)
        c.insert(0, "dt-idx")  # add the datetime index

        for row in data.itertuples():
            cl = row[c.index("close")]
            gap = algoParams["algo_specific"]["enter_confirmation_per"]
            high = orb_high + (orb_high * gap / 100)
            low = orb_low - (orb_low * gap / 100)
            # print(row)
            if cl > high:
                tgt = cl + ((cl * algoParams["controls"]["target_per"]) / 100)
                sl = cl - ((cl * algoParams["controls"]["stoploss_per"]) / 100)

                results.at[0, "target"] = tgt
                results.at[0, "stoploss"] = sl
                results.at[0, "entry"] = row[c.index("close")]
                results.at[0, "entry_time"] = row[0]  # time is the index
                results.at[0, "dir"] = "bullish"
                break
            elif cl < low:
                tgt = cl - ((cl * algoParams["controls"]["target_per"]) / 100)
                sl = cl + ((cl * algoParams["controls"]["stoploss_per"]) / 100)

                results.at[0, "target"] = tgt
                results.at[0, "stoploss"] = sl
                results.at[0, "entry"] = row[c.index("close")]
                results.at[0, "entry_time"] = row[0]  # time is the index
                results.at[0, "dir"] = "bearish"
                break

    except Exception as e:
        results.at[0, "dir"] = "Data Error"
        return results

    finally:
        sl = results.at[0, "stoploss"]

        d = lib_btfn.dbg(d, "08:30", orb_low, "orb_low", "hline|--|red")
        d = lib_btfn.dbg(d, "08:30", orb_high, "orb_high", "hline|-.|green")
        d = lib_btfn.dbg(d, "08:30", sl, "sl", "hline|-.|darkorange")
        d = lib_btfn.dbg_enter(d, results)

        json_object = json.dumps(d)
        results.at[0, "debug_entr"] = json_object
        return results


def _exit(
    algoID,
    symbol,
    df,
    date,
    algoParams,
    pos_dir,
    pos_entr_price,
    pos_entr_time,
    results,
):

    d = []
    s001_sentiment_analyser(df, pos_entr_time, pos_entr_price)

    results.at[0, "debug_exit"] = "[{}]"
    results.at[0, "exit_reason"] = ""

    # --------------------------------------------------------------------- sl & target
    stls = (algoParams["controls"]["stoploss_per"] / 100) * pos_entr_price
    tgt = (algoParams["controls"]["target_per"] / 100) * pos_entr_price

    # --------------------------------------------------------------------- filter cdl (with delayed sl)
    dly_sl = algoParams["controls"]["delayed_stoploss_seconds"]
    # posentr = datetime.strptime(pos_entr_time, "%Y-%m-%d %H:%M:%S")

    if dly_sl != 0:
        start_time = pos_entr_time + timedelta(seconds=dly_sl)
    else:
        start_time = pos_entr_time
    end_time = start_time.replace(hour=15, minute=16, second=0)

    active_cdls = libCdl.filterCandles(
        df,
        start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time.strftime("%Y-%m-%d %H:%M:%S"),
    )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Bullish
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    movment = 0
    if pos_dir.lower() == "bullish":
        # ------------------------------------------------------------------------- scan all candles
        for index, row in active_cdls.iterrows():

            # print(row)
            # --------------------------------------------------------------------- trail calculations
            if (
                row["close"] > pos_entr_price
            ):  # ---------------------------------- if price moved in direction
                curr_mov = row["close"] - pos_entr_price
                if curr_mov > movment:  # new movement higher than previous
                    movment = curr_mov

            # print("movment:", movment)

            if algoParams["controls"]["target_trail_enabled"]:
                target = (pos_entr_price + movment) + tgt

            if algoParams["controls"]["stoploss_trail_enabled"]:
                sl = (pos_entr_price + movment) - stls

            if row["close"] > target:  # ------------------------- target hit
                results = lib_fn.res_exit(results, index, row, "sl")
                break

            elif row["close"] < sl:  # -------- stoploss hit
                results = lib_fn.res_exit(results, index, row, "sl")
                break

            d = lib_btfn.dbg_exit(d, results)
            json_object = json.dumps(d)
            results.at[0, "debug_exit"] = json_object
            return results

        results, ret = lib_fn.eod(df, results)
        if ret:
            return results

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Bearish
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif pos_dir.lower() == "bearish":
        # ------------------------------------------------------------------------- scan all candles
        for index, row in active_cdls.iterrows():

            # --------------------------------------------------------------------- trail calculations
            if (
                row["close"] < pos_entr_price
            ):  # ---------------------------------- if price moved in direction
                movment = pos_entr_price - row["close"]
            else:
                movment = 0

            if algoParams["controls"]["target_trail_enabled"]:
                target = (pos_entr_price - movment) - tgt

            if algoParams["controls"]["stoploss_trail_enabled"]:
                sl = (pos_entr_price - movment) + stls

            if (
                row["close"] > pos_entr_price + target
            ):  # ------------------------- target hit
                return lib_fn.res_exit(results, index, row, "target")
            elif row["close"] < (pos_entr_price - sl):  # -------- stoploss hit
                return lib_fn.res_exit(results, index, row, "sl")

    results, ret = lib_fn.eod(df, results)
    if ret:
        return results

    else:
        return results

    return results


def s001_sentiment_analyser(df, pos_entr_time, pos_entr_price):

    return 0


# Scan date to be used for backtesting, else use current date for real trading
def trade_date(date):
    date_time_obj = datetime.strptime(date, "%Y-%m-%d")

    if date_time_obj.date() != datetime.today().date():
        timeStamp = date + " 09:30:00"
    else:
        timeStamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    return timeStamp
