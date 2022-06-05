from App.DB import tsDB
import datetime
import pandas as pd
from sqlalchemy import text

dbConn = tsDB.dbConnect()

date = '2022-03-16'
table = 'ticks'

for x in range(0, 1, 1):
    current_date_temp = datetime.datetime.strptime(date, "%Y-%m-%d")
    new_date = current_date_temp + datetime.timedelta(days=x)
    dateFetch = new_date.strftime("%Y-%m-%d")

    sql = f"SELECT * FROM ticks WHERE time LIKE '{dateFetch}%' AND symbol LIKE '%-FUT';"
    df = pd.read_sql(text(sql), dbConn)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # print(df.head(10))

    # df = tsDB.fetchTicks(dbConn, dateFetch, table)
    filename = 'ticks_nsefut' + '-' + dateFetch + '(' + str(len(df)) + ').csv'
    print(filename)
    if len(df) > 0:
        df.to_csv('Data/' + table + '/' + filename, index=False)

    sql = f"SELECT * FROM ticks WHERE time LIKE '{dateFetch}%' AND symbol NOT LIKE '%-FUT';"
    df = pd.read_sql(text(sql), dbConn)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # print(df.head(10))

    # df = tsDB.fetchTicks(dbConn, dateFetch, table)
    filename = 'ticks_nsestk' + '-' + dateFetch + '(' + str(len(df)) + ').csv'
    print(filename)
    if len(df) > 0:
        df.to_csv('Data/' + table + '/' + filename, index=False)
