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

# Configuration Data
TARGET_PERCENTAGE = 1.1
ENTRY_GAP_DELTA_PERCENTAGE = 0
ORB_SCAN_CANDLES = 5 # val * 1min candles

STOP_LOSS = '1'
SL_DELAY = '00Min' #('30Min' '0Min' '') < only these 3 are valid entries. Otherwise it breaks!
DEEP_STOPLOSS = '1' # In %

STALL_DETECT_PERIOD = '30Min' # in Minutes
TRAGET_TRAIL = '1'
POS_REVERSAL = '1'
CANDLE_INTERVAL = '5Min'

def S01_ORB_Force(filteredDayDF, selectedDate, results):
    
    try:
        
        results.at[0, 'StopLoss'] = STOP_LOSS
        results.at[0, 'DelayedStopLoss'] = SL_DELAY
        results.at[0, 'StallDetectPeriod'] = STALL_DETECT_PERIOD
        results.at[0, 'TrailTarget'] = TRAGET_TRAIL
        results.at[0, 'PositionRevarsal'] = POS_REVERSAL
        
        results.at[0, 'Strategy'] = 'ORB-Force'
        results.at[0, 'Csize'] = CANDLE_INTERVAL
        results.at[0, 'Date'] = selectedDate        
    
        orb_low, orb_high, day_low, day_high = getORB(filteredDayDF,ORB_SCAN_CANDLES)
        
        cdl_926 = 0 # getTimeCandle(filteredDayDF, 'Close', selectedDate + ' 09:25')
        cdl_926open = 0 #getTimeCandle(filteredDayDF, 'Open', selectedDate + ' 09:25')
        cdl_930 = 0 #getTimeCandle(filteredDayDF, 'Close', selectedDate + ' 09:30')
        #cdl_315 = getTimeCandle(       filteredDayDF, 'Close', selectedDate + ' 15:15')

        orbDelta = ((abs(orb_high-orb_low)*ENTRY_GAP_DELTA_PERCENTAGE)/100)

        if (cdl_930 > (orb_high + orbDelta)):
            if (cdl_930 > cdl_926open): #Green candle
                results.at[0, 'Signal'] = 'Bullish'
                results.at[0, 'Target'] = cdl_930 + (cdl_930*TARGET_PERCENTAGE/100)
                results.at[0, 'DeepStopLoss'] = (cdl_930*DEEP_STOPLOSS/100)
                results.at[0, 'StopLoss'] = cdl_926open
                results.at[0, 'Entry'] = cdl_930
                results.at[0, 'EntryTime'] = '09:30'
            else:
                results.at[0, 'Signal'] = 'Failed Bullish'


        elif (cdl_930 < (orb_low - orbDelta)):
            if (cdl_930 < cdl_926open): # Red candle
                results.at[0, 'Signal'] = 'Bearish'
                results.at[0, 'Target'] = cdl_930 - (cdl_930*TARGET_PERCENTAGE/100)
                results.at[0, 'StopLoss'] = cdl_926open
                results.at[0, 'DeepStopLoss'] = (cdl_930*DEEP_STOPLOSS/100)
                results.at[0, 'Entry'] = cdl_930
                results.at[0, 'EntryTime'] = '09:30'
            else:
                results.at[0, 'Signal'] = 'Failed Bearish'

        else:
            results.at[0, 'Signal'] = 'NA'
            
            
    except Exception as e:
        print('Data Error', selectedDate)
        print (e)
        results.at[0, 'Signal'] = 'Data Error'
        return results

    else: 
        return results
    