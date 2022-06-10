import App.Libraries as lib
import pandas as pd


##########################################################################
#                    Filter specific candle
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Arg: Input DF, Column (open, close...), Time
# Ret: Cell Value
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getTimeCandle(Xdf, Xcol, Xtime):
    # print(Xdf.at[Xtime, Xcol][0])
    return Xdf.at[Xtime, Xcol][0]


ohlc_dict = {
    'open': 'first',
    'high': 'max',
    'low': 'min',
    'close': 'last',
    'symbol': 'first',
    'volume': 'sum',
    'buy_demand': 'median',
    'sell_demand': 'median',
    'open_interest': 'median'
}


def CdlConv(df, freq):

    try:

        df['time'] = pd.to_datetime(df['time'])
        df = df.set_index('time')
        summary = pd.DataFrame(columns=None)

        # get unique symbols
        symlist = df.symbol.unique()

        for x in symlist:
            df1 = df[df['symbol'] == x]
            df1 = df1.resample(freq, closed='left',
                               label='left').apply(ohlc_dict)
            summary = summary.append(df1)

    except Exception as e:
        # print(e)
        summary = pd.DataFrame(columns=None)

    return summary


def TickToCdl(df, date, freq):

    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    dfCdl = pd.DataFrame(columns=None)

    # get unique symbols
    symlist = df.symbol.unique()

    for x in symlist:
        df1 = df[df['symbol'] == x]

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

        dfCdl = dfCdl.append(dfmerged)

    return dfCdl
