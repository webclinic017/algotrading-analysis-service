from App.DB import tsDB
# import datetime
import pandas as pd
from glob import iglob
from sqlalchemy import text

BASE_PATH = "/home/parag/devArea/algotrading-analysis-service/Data"
SUB_PATH_FUT = '/1min_nsefut/'
SUB_PATH_STK = '/1min_nsestk/'


def CreateCandlesInDb(dbconn, date, freq, db_name):

    sql = f"SELECT * FROM {db_name}  WHERE time LIKE '{date}%';"
    df = pd.read_sql(text(sql), conn)
    # print(df.head(10))
    df['time'] = pd.to_datetime(df['time'])
    # print(df.head(10))
    df = df.set_index('time')
    # print(df.head(10))
    summary = pd.DataFrame()

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
        # dfmerged.drop(['trades_till_now'], axis=1, inplace=True)

        # dfmerged.to_csv("check.csv")

        summary = summary.append(dfmerged)

    return summary, len(symlist), len(summary)


conn = tsDB.dbConnect()

sql = f"SELECT DISTINCT(DATE(time)) FROM ticks_nsestk_lcl;"
dfDates = pd.read_sql(text(sql), conn)

for x in range(len(dfDates)):
    df, symCnt, rows = CreateCandlesInDb(conn, dfDates.iloc[x]['date'], '1T',
                                         'ticks_nsestk_lcl')
    f = BASE_PATH + SUB_PATH_STK + str(
        dfDates.iloc[x]['date']) + ' ( Symbols ' + str(
            symCnt) + ' - Rows ' + str(rows) + ' ).csv'
    df.to_csv(f)

sql = f"SELECT DISTINCT(DATE(time)) FROM ticks_nsefut_lcl;"
dfDates = pd.read_sql(text(sql), conn)

for x in range(len(dfDates)):
    df, symCnt, rows = CreateCandlesInDb(conn, dfDates.iloc[x]['date'], '1T',
                                         'ticks_nsefut_lcl')
    f = BASE_PATH + SUB_PATH_FUT + str(
        dfDates.iloc[x]['date']) + ' ( Symbols ' + str(
            symCnt) + ' - Rows ' + str(rows) + ' ).csv'
    df.to_csv(f)
