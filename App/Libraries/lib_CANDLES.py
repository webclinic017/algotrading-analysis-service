##########################################################################
#                    Filter specific candle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arg: Input DF, Column (open, close...), Time
# Ret: Cell Value
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getTimeCandle( Xdf, Xcol, Xtime):
    idx = Xdf.index.get_loc(Xtime)
    return Xdf.iloc[idx][Xcol]


##########################################################################
#                    Resample candle from 1Min to xMin
# Function - if candle before 9:15 copy to next and generate candles
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arg: Input DF, Sample period
# Ret: DF
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def convertCandleSize (selectedDate, dataDF, cdlSize):
    
    
    try:

        # check if candle(s) before 09:16 is present, then copy to 09:16(next) and delete
        cdl0908DF = dataDF.loc[dataDF.index <  selectedDate + ' 09:15']

        if not cdl0908DF.empty:

            # check if more than one candle before 09:16
            if (len(cdl0908DF.index) == 1):

                # we will remove the first entry @ 09:08 and copy Open to 9:15 candle
                dataDF.at[dataDF.index[1], 'Open'] = dataDF.at[dataDF.index[0], 'Open']

                # Remove the frist entry 09:08
                dataDF.drop(dataDF.head(1).index, inplace=True)
                # resample to new timedelta
                dataDF = dataDF.resample(cdlSize, closed='right').agg({ 'Open': lambda s: s[0], \
                                              'High': lambda dataDF: dataDF.max(),\
                                              'Low': lambda dataDF: dataDF.min(),\
                                              'Close': lambda dataDF: dataDF[-1]})
                return dataDF

            else:
                print("ERR: lib_CANDLES - More than one candle before 09:16")

        else:
            # resample to new timedelta
            dataDF = dataDF.resample(cdlSize, closed='right').agg({ 'Open': lambda s: s[0], \
                                              'High': lambda s: s.max(),\
                                              'Low': lambda s: s.min(),\
                                              'Close': lambda s: s[-1]})
            return dataDF
    
    except Exception as e:
        print ("lib_CANDLES/convertCandleSize() Data Error", selectedDate, e)
        #print(selectedDate, dataDF, cdlSize)
        
        
        return dataDF
