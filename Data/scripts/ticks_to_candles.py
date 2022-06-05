# from App.DB import tsDB
# import datetime
import pandas as pd
from glob import iglob

# dbConn = tsDB.dbConnect()

date = '2022-04-04'
path = r'/home/parag/devArea/algotrading-analysis-service/Data/src/*.csv'

df = pd.concat((pd.read_csv(f, sep=',') for f in iglob(path, recursive=True)),
               ignore_index=True)

df['Datetime'] = pd.to_datetime(df['time'])
df = df.set_index('Datetime')

# get unique symbols
symlist = df.symbol.unique()

for x in symlist:
    df1 = df[df['symbol'] == x]
    df1.to_csv(x + 'raw.csv')
    print(len(df1))
    freq = '1T'

    dfmerged = df1['last_traded_price'].resample(freq).ohlc()
    dfmerged['volume'] = df1['trades_till_now'].resample(
        '1T').last() - df1['trades_till_now'].resample(freq).first()

    dfmerged['buy_demand'] = df1['buy_demand'].resample(freq).median()
    dfmerged['sell_demand'] = df1['sell_demand'].resample(freq).median()

    dfmerged['open_interest'] = df1['open_interest'].resample(freq).median()

    print(len(dfmerged))
    dfmerged.to_csv(x + '-m.csv')
