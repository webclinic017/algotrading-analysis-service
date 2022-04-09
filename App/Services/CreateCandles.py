from App.DB import tsDB
# import datetime
import pandas as pd
from glob import iglob


def CreateCandlesInDb(dbconn, date, freq):

    df = tsDB.fetchTicksData(dbconn, date)
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

        dfmerged.to_csv("check.csv")

        # write to DB
        tsDB.saveCandles(dbconn, dfmerged)


# TODO: Offline data check for generated data required by
# TODO: Candle check in tick_ db and this db to be checked
