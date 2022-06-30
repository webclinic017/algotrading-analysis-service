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


def analysis(algoID, mode, symbol, df, date, algoParams, pos_dir,
             pos_entr_price, pos_entr_time, results):

    if mode == "entr":
        _entr(algoID, symbol, df, date, algoParams, results)
    elif mode == "exit":
        _exit(algoID, symbol, df, date, algoParams, pos_dir, pos_entr_price,
              pos_entr_time, results)
    else:
        results.at[0, "status"] = "ERR: Invalid mode " + mode

    return results


def _entr(algoID, symbol, df, date, algoParams, results):

    debug_list = []

    #--------------------------------------------------------------
    # Minimum data to be returned - status,date,instr,strategy,dir |
    #--------------------------------------------------------------
    results.at[0, "instr"] = symbol
    results.at[0, "strategy"] = algoID
    results.at[0, "date"] = trade_date(date)
    results.at[0, "status"] = "pending"
    results.at[0, "dir"] = "NA"
    #-------------------------------------------------------------

    #--------------------------------------------------------------
    # Strategy                                                    |
    #--------------------------------------------------------------

    try:
        print("place holder")

    except Exception as e:
        results.at[0, "dir"] = "Data Error"
        return results

    finally:

        debug_list.append({
            'variable': 'none',
            'value-x': "09:30",
            'value-y': str(0),
            'value-print': '',
            'drawing': 'vline',
            'draw_fill': 'dotted',
            'draw_color': 'purple'
        })

        json_object = json.dumps(debug_list)

        results.at[0, "debug"] = json_object
        return results


def debug_list_add(dbg, var, vx, vy, val_print, drwg, drw_fill, drw_clr):
    dbg.append({
        'variable': var,
        'value-x': vx,
        'value-y': str(vy),
        'value-print': str(val_print),
        'drawing': drwg,
        'draw_fill': drw_fill,
        'draw_color': drw_clr
    })
    return dbg


def _exit(algoID, symbol, df, date, algoParams, pos_dir, pos_entr_price,
          pos_entr_time, results):

    s001_sentiment_analyser(df, pos_entr_time, pos_entr_price)

    # --------------------------------------------------------------------- sl & target
    stls = (algoParams["controls"]["stoploss_per"]) * pos_entr_price
    tgt = (algoParams["controls"]["target_per"]) * pos_entr_price

    # --------------------------------------------------------------------- filter cdl (with delayed sl)
    dly_sl = algoParams["controls"]["delayed_stoploss_seconds"]
    posentr = datetime.strptime(pos_entr_time, "%Y-%m-%d %H:%M:%S")

    if dly_sl != 0:
        start_time = posentr + timedelta(seconds=dly_sl)
    else:
        start_time = posentr
    end_time = start_time.replace(hour=15, minute=16, second=0)

    active_cdls = libCdl.filterCandles(
        df, start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time.strftime("%Y-%m-%d %H:%M:%S"))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Bullish
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if pos_dir.lower() == "bullish":
        # ------------------------------------------------------------------------- scan all candles
        for index, row in active_cdls.iterrows():

            # print(row)
            # --------------------------------------------------------------------- trail calculations
            if row['close'] > pos_entr_price:  # ---------------------------------- if price moved in direction
                movment = row['close'] - pos_entr_price
            else:
                movment = 0

            if algoParams['controls']['target_trail_enabled']:
                target = (pos_entr_price + movment) + tgt

            if algoParams['controls']['stoploss_trail_enabled']:
                sl = (pos_entr_price + movment) - stls

            if row['close'] > pos_entr_price + target:  # ------------------------- target hit
                results.at[0, "exit_time"] = index
                results.at[0, "exit"] = row['close']
                results.at[0, "exit_reason"] = "target"
                results.at[0, "status"] = "signal-processed"
                return results

            elif row['close'] < (pos_entr_price - sl):  # -------- stoploss hit
                results.at[0, "exit_time"] = index
                results.at[0, "exit"] = row['close']
                results.at[0, "exit_reason"] = "sl/deepsl"
                results.at[0, "status"] = "signal-processed"
                return results

        start_time = posentr.replace(hour=15, minute=16, second=0)
        end_time = posentr.replace(hour=15, minute=31, second=0)

        eod_cdls = libCdl.filterCandles(
            df, start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"))

        if len(eod_cdls):
            row = eod_cdls.iloc[0]
            results.at[0, "exit_time"] = index
            results.at[0, "exit"] = row['close']
            results.at[0, "exit_reason"] = "eod"
            results.at[0, "status"] = "signal-processed"
            return results

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Bearish
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif pos_dir.lower() == "bearish":
        # ------------------------------------------------------------------------- scan all candles
        for index, row in active_cdls.iterrows():

            # --------------------------------------------------------------------- trail calculations
            if row['close'] < pos_entr_price:  # ---------------------------------- if price moved in direction
                movment = pos_entr_price - row['close']
            else:
                movment = 0

            if algoParams['controls']['target_trail_enabled']:
                target = (pos_entr_price - movment) - tgt

            if algoParams['controls']['stoploss_trail_enabled']:
                sl = (pos_entr_price - movment) + stls

            if row['close'] > pos_entr_price + target:  # ------------------------- target hit
                results.at[0, "exit_time"] = index
                results.at[0, "exit"] = row['close']
                results.at[0, "exit_reason"] = "target"
                results.at[0, "status"] = "signal-processed"
                return results
            elif row['close'] < (pos_entr_price - sl):  # -------- stoploss hit
                results.at[0, "exit_time"] = index
                results.at[0, "exit"] = row['close']
                results.at[0, "exit_reason"] = "sl/deepsl"
                results.at[0, "status"] = "signal-processed"
                return results

        start_time = posentr.replace(hour=15, minute=16, second=0)
        end_time = posentr.replace(hour=15, minute=31, second=0)

        eod_cdls = libCdl.filterCandles(
            df, start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"))

        if len(eod_cdls):
            row = eod_cdls.iloc[0]
            results.at[0, "exit_time"] = index
            results.at[0, "exit"] = row['close']
            results.at[0, "exit_reason"] = "eod"
            results.at[0, "status"] = "signal-processed"
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