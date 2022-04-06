# from App.DB import tsDB
# import datetime
import pandas as pd
from glob import iglob

# dbConn = tsDB.dbConnect()

date = '2022-04-04'
path = r'/home/parag/devArea/algotrading-analysis-service/Data/src/*.csv'

# df = pd.read_csv(path, parse_dates=["date"], index_col="date")

df = pd.concat((pd.read_csv(f, sep=',') for f in iglob(path, recursive=True)),
               ignore_index=True)

print(df)
df['Datetime'] = pd.to_datetime(df['time'])
df = df.set_index('Datetime')

symlist = df.symbol.unique()

for x in symlist:
    df1 = df[df['symbol'] == x]
    print(len(df1))
    df1 = df1.drop(columns=[
        'time', 'symbol', "buy_demand", "sell_demand", "trades_till_now",
        "open_interest"
    ])
    print(df1)
    df1 = df1.resample('1T').ohlc()
    print(len(df1))
    df1.to_csv(x + '.csv')

# "time", "symbol", "last_traded_price"

# df.set_index('time', inplace=True)

# for x in range(0, 1, 1):
#     current_date_temp = datetime.datetime.strptime(date, "%Y-%m-%d")
#     new_date = current_date_temp + datetime.timedelta(days=x)
#     dateFetch = new_date.strftime("%Y-%m-%d")
#     df = tsDB.fetchTicksData(dbConn, dateFetch)
#     print(len(df))
#     df.to_csv(dateFetch + '.csv')

# https://stackoverflow.com/questions/36222928/pandas-ohlc-aggregation-on-ohlc-data
# def ohlcVolume(x):
#     if len(x):
#         ohlc={ "open":x["open"][0],"high":max(x["high"]),"low":min(x["low"]),"close":x["close"][-1],"volume":sum(x["volume"])}
#         return pd.Series(ohlc)

# daily=df.resample('1D').apply(ohlcVolume)