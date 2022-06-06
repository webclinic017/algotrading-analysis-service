##########################################################################
#                    Filter specific candle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arg: Input DF, Column (open, close...), Time
# Ret: Cell Value
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getTimeCandle(Xdf, Xcol, Xtime):
    # print(Xdf.at[Xtime, Xcol][0])
    return Xdf.at[Xtime, Xcol][0]


##########################################################################
#                    Resample candle from 1Min to xMin
# Function - if candle before 9:15 copy to next and generate candles
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arg: Input DF, Sample period
# Ret: DF
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def convertCandleSize(selectedDate, dataDF, cdlSize):

    from App.DB import tsDB


# import datetime
import pandas as pd
from glob import iglob


def CdlConv(df, freq):

    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')

    # get unique symbols
    symlist = df.symbol.unique()

    for x in symlist:
        df1 = df[df['symbol'] == x]
        df1.to_csv("check-org.csv")

        # ohlc
        dfmerged = df1['last_traded_price'].resample(freq).ohlc()

        # volume
        dfmerged['volume'] = df1['trades_till_now'].resample(
            '1T').last() - df1['trades_till_now'].resample(freq).first()

        # buy_demand & sell_demand
        dfmerged['buy_demand'] = df1['buy_demand'].resample(freq).median()
        dfmerged['sell_demand'] = df1['sell_demand'].resample(freq).median()

        # open_interest
        dfmerged['open_interest'] = df1['open_interest'].resample(
            freq).median()

        # symbol
        dfmerged['symbol'] = x
        # dfmerged.drop(['trades_till_now'], axis=1, inplace=True)
    return dfmerged