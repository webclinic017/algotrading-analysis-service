
RESULTS_HEADER = ['Strategy', 'Date', 'Csize', 'Signal', \
                  'Entry', 'EntryTime', 'Target', 'SL', 'Exit', 'ExitTime', 'Reason', 'Result', 'ResultPerc', \
                         'SMax', 'SMaxD','SMaxTime', 'SMin', 'SMinD','SMinTime', 'ExitCriteria']


import numpy as np
import pandas as pd
from time import strftime
from App.Libraries.lib_BACKTEST import btResultsParser

def IntraDay_Directional_NakedPosition (dayDF, selectedDate, strategy):

    # # if signal received
    # if strategyScan.at[0, 'Signal'] == 'Bullish' or strategyScan.at[0, 'Signal'] == 'Bearish':
        
    #     pPositionReversal = strategy.at[0, 'PositionRevarsal']
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #     # Bullish
    #     # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     
        
                
    #         # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #         # Check for Target acheived
    #         # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #         pTargetTrail = strategy.at[0, 'TrailTarget']
            
    #         Tgtmask = cdlDF['Close'] > (strategy.at[0, 'Target'])
    #         tgtDF = cdlDF.loc[Tgtmask]
    #         if (len(tgtDF) > 0):
    #             idx = tgtDF.index[0]
    #             strategy.at[0, 'Exit'] = cdlDF.at[idx, 'Close']
    #             strategy.at[0, 'ExitTime'] = idx.time().strftime("%H:%M")
    #             strategy.at[0, 'Reason'] = 'Target'
                
                
    #         strategy.at[0, 'Result'] = strategy.at[0, 'Exit'] - strategy.at[0, 'Entry']
            
    return 0


# ToDo: Could add logic to run multiple scans on same date as in case of real world

# btResultsParser(BTresults, NIFTY_DATA_FILTER)


