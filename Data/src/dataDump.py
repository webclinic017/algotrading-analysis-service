from App.DB import tsDB
import datetime
import pandas as pd

dbConn = tsDB.dbConnect()

date = '2022-04-04'

for x in range(0, 1, 1):
    current_date_temp = datetime.datetime.strptime(date, "%Y-%m-%d")
    new_date = current_date_temp + datetime.timedelta(days=x)
    dateFetch = new_date.strftime("%Y-%m-%d")
    df = tsDB.fetchTicksData(dbConn, dateFetch)
    print(len(df))
    df.to_csv(dateFetch + '.csv')
