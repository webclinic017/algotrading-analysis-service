def analyseSentinments(activeCdls, strategy):
    #print(period)
    # 1. count green/red candles. > 50% gives direction
    # 2. size of green/red determines the force in the direction
    # 3. Return interpreted status    
    return 0


# %%
def controlStopLoss(activeCdls, strategy):
    
    pSl = strategy.at[0, 'StopLoss']
    pSlDeep = float(strategy.at[0, 'DeepStopLoss'])    
    
    if strategy.at[0, 'Signal'] == 'bullish':
        
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



def jumpToActiveCandles(dayDF, selectedDate, strategy):

    pSlDelay = strategy.at[0, 'DelayedStopLoss']
   
    entryTime = selectedDate + ' ' + strategy.at[0, 'EntryTime']
    # filter candles from the point of position entry time in strategy and add delay if applicable
    activeTime = pd.Timestamp(entryTime) + pd.Timedelta(pSlDelay)
    dayDF = dayDF.loc[dayDF.index >  activeTime]

    return dayDF;
    

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EoD exit - Common Routine ? (right now part of bullish)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if np.isnan(strategy.at[0, 'Exit']):
    mask = cdlDF.index >  selectedDate + ' 15:15' #blank space required for string of date/time
    eodDF = cdlDF.loc[mask]
    if not eodDF.empty:
        idx = eodDF.index[0]
        strategy.at[0, 'Exit'] = eodDF.at[idx, 'Close']
        strategy.at[0, 'ExitTime'] = idx.time().strftime("%H:%M")
        strategy.at[0, 'Reason'] = 'EoD'    