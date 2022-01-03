# %% [markdown]
# # Trading Engine
# 
# > Trades are directional and naked positions
# 

# %%
# Date Filter
NIFTY_DATA_FILTER = '2021' #'2020_02'

# %%
# Configuration Data
cNIFTY50 = 'nifty50'
cNIFTYBANK = 'banknifty'
BASE_PATH = "/home/parag/devArea/pyStock"

RESULTS_HEADER = ['Strategy', 'Date', 'Csize', 'Signal', \
                  'Entry', 'EntryTime', 'Target', 'SL', 'Exit', 'ExitTime', 'Reason', 'Result', 'ResultPerc', \
                         'SMax', 'SMaxD','SMaxTime', 'SMin', 'SMinD','SMinTime', 'ExitCriteria']

# %%1
# Import paths
import os
import sys
import time
import numpy as np
import pandas as pd
from tqdm import tqdm
from time import strftime
import matplotlib.pyplot as plt

# Importing libraries
sys.path.append(BASE_PATH+'/Libraries/')
from lib_STOCK import readStockData
from lib_CANDLES import convertCandleSize
from lib_BACKTEST import btEngine, btResultsParser
from lib_ENCODE import readExitCriteria

sys.path.append(BASE_PATH+'/Strategies/')
from S01_ORB import S01_ORB_Force

BNFs, df_dates = readStockData(BASE_PATH, NIFTY_DATA_FILTER, cNIFTYBANK)

# %%
def analyseSentinments(activeCdls, strategy):
    #print(period)
    # 1. count green/red candles. > 50% gives direction
    # 2. size of green/red determines the force in the direction
    # 3. Return interpreted status    
    
    
    return 0

def jumpToActiveCandles(dayDF, selectedDate, strategy):

    pSlDelay = strategy.at[0, 'DelayedStopLoss']
   
    entryTime = selectedDate + ' ' + strategy.at[0, 'EntryTime']
    # filter candles from the point of position entry time in strategy and add delay if applicable
    activeTime = pd.Timestamp(entryTime) + pd.Timedelta(pSlDelay)
    dayDF = dayDF.loc[dayDF.index >  activeTime]

    return dayDF;
    
    
def recordExtremes(dayDF, selectedDate, strategy):
    
    max_index = dayDF["Close"].idxmax()
    min_index = dayDF["Close"].idxmin()
        
    strategy.at[0, 'SMax'] = dayDF.at[max_index, 'Close']
    strategy.at[0, 'SMaxTime'] = pd.to_datetime(max_index).time().strftime("%H:%M")
    strategy.at[0, 'SMaxD'] = strategy.at[0, 'SMax'] - strategy.at[0, 'Entry']

    strategy.at[0, 'SMin'] = dayDF.at[min_index, 'Close']
    strategy.at[0, 'SMinTime'] = pd.to_datetime(min_index).time().strftime("%H:%M")
    strategy.at[0, 'SMinD'] = strategy.at[0, 'Entry'] - strategy.at[0, 'SMin']

    return
     

# %%
def controlStopLoss(activeCdls, strategy):
    
    pSl = strategy.at[0, 'StopLoss']
    pSlDeep = float(strategy.at[0, 'DeepStopLoss'])    
    
    if strategy.at[0, 'Signal'] == 'Bullish':
        
        slDF = pd.DataFrame()
        pSl =  (strategy.at[0, 'StopLoss']) - (strategy.at[0, 'DeepStopLoss'])
        SLmask = cdlDF['Close'] < pSl
        slDF = cdlDF.loc[SLmask]

        if (len(slDF) > 0):
            #if SL detected
            idx = slDF.index[0]
            strategy.at[0, 'Exit'] = cdlDF.at[idx, 'Close']
            strategy.at[0, 'ExitTime'] = idx.time().strftime("%H:%M")
            if (pSlDeep != 0): # check pSlDeep
                strategy.at[0, 'Reason'] = 'SL Deep'
            else:
                strategy.at[0, 'Reason'] = 'StopLoss'
    

# %%
# TradeEngine operational logics (selected based on Strategies encoded)
# This loop runs once for one strategy
    # 1 - SL
    # 2 - DeepSL
    # 3 - Delayed SL
    # 4 - Sentiments - Gravity, Priming, Stall
    # 5 - EoD exit - If no exit conditions prevailed, add exit at 15:15
    
    # ToDo: scan based on candle intervals
    # ToDo: SL delayed interval - add data to strategy module, only parse here
    # ToDo: Fine tune ORB - check what you have missed, vefiry in charts. May be later once engine is ready?


def IntraDay_Directional_NakedPosition (dayDF, selectedDate, strategy):

    # if signal received
    if strategyScan.at[0, 'Signal'] == 'Bullish' or strategyScan.at[0, 'Signal'] == 'Bearish':
        
        activeCdls = jumpToActiveCandles(dayDF, selectedDate, strategy)
    
 

        
        
        pPositionReversal = strategy.at[0, 'PositionRevarsal']

        analyseSentinments(activeCdls, strategy)
        
        cdlDF = convertCandleSize(selectedDate, activeCdls, strategy.at[0, 'Csize'])
        

        controlStopLoss(activeCdls, strategy)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Bullish
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     
        
                
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
        #elif strategy.at[0, 'Signal'] == 'Bearish':
            #print('bearish')
            #if len(slDF) > 0 :
                #strategy.at[0, 'Position Exit'] == slDF.at[1, 'Close']
                #strategy.at[0, 'Position Exit time'] == slDF.at[0, index]
             #   print(slDF)


            #print(slDF)

            
            #print('no exits trigerred, check EoD candle')
            #print('exit', strategy.at[0, 'Exit'])
            #type(strategy.at[0, 'Exit'])
            
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # EoD exit - Common Routine ? (right now part of Bullish)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            if np.isnan(strategy.at[0, 'Exit']):
                mask = cdlDF.index >  selectedDate + ' 15:15' #blank space required for string of date/time
                eodDF = cdlDF.loc[mask]
                if not eodDF.empty:
                    idx = eodDF.index[0]
                    strategy.at[0, 'Exit'] = eodDF.at[idx, 'Close']
                    strategy.at[0, 'ExitTime'] = idx.time().strftime("%H:%M")
                    strategy.at[0, 'Reason'] = 'EoD'
                

            
            strategy.at[0, 'Result'] = strategy.at[0, 'Exit'] - strategy.at[0, 'Entry']
            


        recordExtremes(activeCdls, selectedDate, strategy)
#     else:
#         print("no signal")
# return 0
    

# %%


# %%
# clear results
BTresults = pd.DataFrame(columns=RESULTS_HEADER)

# %%
# read encoded data
from lib_ENCODE import readExitCriteria
# run strategy and backtest on every date

# ToDo: Could add logic to run multiple scans on same date as in case of real world

for i, values in tqdm(df_dates.iterrows(), total=df_dates.shape[0], colour='green'):
    selectedDate = i.strftime('%Y%m%d')   #Convert datetime to string
    filteredDayDF = BNFs.loc[selectedDate]

    # run strategy scan
    strategyScan = pd.DataFrame(columns=RESULTS_HEADER)
    strategyScan = S01_ORB_Force(filteredDayDF, selectedDate, strategyScan)
    
    # run backtest if signal detected
    tradeEngine_IntraDay_Directional_NakedPosition(filteredDayDF, selectedDate, strategyScan)
    
    # append results
    BTresults = BTresults.append(strategyScan,ignore_index=True,sort=False)
    del strategyScan
    

# %%
btResultsParser(BTresults, NIFTY_DATA_FILTER)

# %%



