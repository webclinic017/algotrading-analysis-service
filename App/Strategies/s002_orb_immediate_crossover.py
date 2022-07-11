# ----------------------------------------------------------------
#  Strategy Name - ORB with Immediate Crossover
# ----------------------------------------------------------------


# ----------------------------DATA--------------------------------
#
# Candle Size   #1 Min
# Subscription -
#
# ---------------------------ENTRY--------------------------------
#
# (cdl_close) > (orb_high + {enter_confirmation_per} )
# (cdl_close) < (orb_low - {enter_confirmation_per} )
#
# ----------------------------EXIT--------------------------------
#
# SL            - Based on cfg param {stoploss_per}
# Target        - Based on cfg param {target_per}
# Sentinment    - Based on cfg param {sentiment_analyser_enabled}
#
# -------------------------ALGO PARAMS----------------------------
#
# ["algo_specific"]
#   -   ["enter_confirmation_per"]
#   -   ["sentiment_period_seconds"]    - Period to be checked [0: disabled, NUM - enabled]
#   -   ["sentiment_buy_sell_gap_per"]  - difference between buy/sell to be considered
# ["controls"]
#   -   ["target_per"]
#   -   ["stoploss_per"]
#   -   ["delayed_stoploss_seconds"]
#   -   ["target_trail_enabled"]
#   -   ["stoploss_trail_enabled"]
#
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


# ----------------------------------------------------------------------------
# ENTER
# ----------------------------------------------------------------------------
def _entr(algoID, symbol, df, date, algoParams, results):

    # ------------------------------------------------------------------------ minimum data
    results.at[0, "instr"] = symbol
    results.at[0, "strategy"] = algoID
    results.at[0, "date"] = date
    results.at[0, "status"] = "pending"
    results.at[0, "dir"] = "NA"
    results.at[0, "debug_entr"] = "{}"

    # ------------------------------------------------------------------------ strategy                                                     |
    try:
        orb = df.between_time("9:15", "9:30")
        # -------------------------------------------------------------------- calculate ORB
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
        # -------------------------------------------------------------------- debug info
        d = []
        sl = results.at[0, "stoploss"]
        tgt = results.at[0, "target"]
        d = lib_btfn.dbg(d, "08:30", orb_low, "orb_low", "hline|solid|red")
        d = lib_btfn.dbg(d, "08:30", orb_high, "orb_high", "hline|solid|green")
        d = lib_btfn.dbg(d, "08:30", sl, "sl", "hline|-.|darkorange")
        d = lib_btfn.dbg(d, "08:30", tgt, "target", "hline|--|darkorange")
        d = lib_btfn.dbg_enter(d, results)
        results.at[0, "debug_entr"] = json.dumps(d)

        return results


# ----------------------------------------------------------------------------
# EXIT
# ----------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------ minimum data
    results.at[0, "debug_exit"] = "[{}]"
    results.at[0, "exit_reason"] = ""

    # ------------------------------------------------------------------------ sl & target
    stls = (algoParams["controls"]["stoploss_per"] / 100) * pos_entr_price
    tgt = (algoParams["controls"]["target_per"] / 100) * pos_entr_price

    # ------------------------------------------------------------------------ filter cdl (with delayed sl)
    dly_sl = algoParams["controls"]["delayed_stoploss_seconds"]

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
    if pos_dir.lower() == "bullish":
        movment = 0

        #                                                                      scan all candles
        for index, row in active_cdls.iterrows():
            cl = row["close"]
            target = tgt
            sl = stls
            # ---------------------------------------------------------------- trail calculations (when price moved in dir)
            if cl > pos_entr_price:
                curr_mov = cl - pos_entr_price
                #                                                              new movement higher than previous
                if curr_mov > movment:
                    movment = curr_mov

            if algoParams["controls"]["target_trail_enabled"]:
                target = (pos_entr_price + movment) + tgt

            if algoParams["controls"]["stoploss_trail_enabled"]:
                sl = (pos_entr_price + movment) - stls

            # ---------------------------------------------------------------- target hit
            if cl > target:
                results = lib_fn.res_exit(results, index, row, "target")
                break

            # ---------------------------------------------------------------- stoploss hit
            elif cl < sl:
                results = lib_fn.res_exit(results, index, row, "sl")
                break

            # ---------------------------------------------------------------- sentiments
            elif _sentiment_reversed(
                algoParams, index, active_cdls, pos_entr_time, "bullish"
            ):
                results = lib_fn.res_exit(results, index, row, "sentiment")
                break

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Bearish
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif pos_dir.lower() == "bearish":
        movment = 0
        #                                                                      scan all candles
        for index, row in active_cdls.iterrows():
            cl = row["close"]
            target = tgt
            sl = stls
            # ---------------------------------------------------------------- trail calculations (if price moved in direction)
            if cl < pos_entr_price:
                curr_mov = pos_entr_price - cl
                if curr_mov > movment:  # new movement higher than previous
                    movment = curr_mov

            if algoParams["controls"]["target_trail_enabled"]:
                target = (pos_entr_price - movment) - tgt

            if algoParams["controls"]["stoploss_trail_enabled"]:
                sl = (pos_entr_price - movment) + stls

            # ---------------------------------------------------------------- target hit
            if cl < target:
                results = lib_fn.res_exit(results, index, row, "target")
                break

            # ---------------------------------------------------------------- stoploss hit
            elif cl > sl:
                results = lib_fn.res_exit(results, index, row, "sl")
                break

            # ---------------------------------------------------------------- sentiments
            elif _sentiment_reversed(
                algoParams, index, active_cdls, pos_entr_time, "bearish"
            ):
                results = lib_fn.res_exit(results, index, row, "sentiment")
                break

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Common Routine
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #                                                                          eod check
    results = lib_fn.eod(df, results)

    # ------------------------------------------------------------------------ debug info
    d = []
    results.at[0, "debug_exit"] = json.dumps(lib_btfn.dbg_exit(d, results))

    return results


# ----------------------------------------------------------------------------
# SENTIMENT ANALYSER
# ----------------------------------------------------------------------------
def _sentiment_reversed(algoParams, index, df, pos_entr_time, dir):

    c = ""
    # -----------------------------------------------------------------------  senti analysis enabled?
    s = algoParams["algo_specific"]["sentiment_period_seconds"]
    if s == 0:
        return False

    # ------------------------------------------------------------------------ scan after gap is covered
    gap = (index - pos_entr_time).total_seconds()
    if gap >= s:
        data = df.loc[index - timedelta(seconds=s - 1) : index]
        b = data["buy_demand"].sum()
        s = data["sell_demand"].sum()

        # -------------------------------------------------------------------- check buyer/seller who is more active
        delta = abs(b - s)
        delta = (delta / (b + s)) * 100
        if delta > algoParams["algo_specific"]["sentiment_buy_sell_gap_per"]:
            if b > s:
                c = "bullish"
            else:
                c = "bearish"
        else:
            c = "stall"
        # --------------------------------------------------------------------- in same direction
        if c == dir:
            return False
        else:
            return True
