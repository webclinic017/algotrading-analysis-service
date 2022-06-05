import datetime
import pandas as pd
from sqlalchemy import text
from os.path import exists
import os
import json
import sqlalchemy

BASE_PATH = "/home/parag/devArea/algotrading-analysis-service/Data/1min_nsefut_zip/"
TABLE = 'ticks_nsefut_zip_lcl'
header_list = [
    'time',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'buy_demand',
    'sell_demand',
    'open_interest',
    'symbol',
]


def dbConnect():  # connect to database

    fileDir = os.path.dirname(os.path.realpath(__file__))
    credentials_file = os.path.join(fileDir, "./../credentials.json")

    if exists(credentials_file):
        f = open(credentials_file, "r")
        credentials = json.load(f)
        f.close()
        prefix = credentials['envprefix']
        db_url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
            database=credentials[prefix + "DB_NAME"],
            host=credentials[prefix + "DB_HOST"],
            user=credentials[prefix + "DB_USER"],
            password=credentials[prefix + "DB_PASS"],
            port=credentials[prefix + "DB_PORT"])

    engine = sqlalchemy.create_engine(db_url)
    return engine


dbConn = dbConnect()

sql = f"SELECT DISTINCT(DATE(time)) FROM {TABLE};"
dfDates = pd.read_sql(text(sql), dbConn)

for x in range(len(dfDates)):
    print(x, 'of', len(dfDates))
    sql = f"SELECT * FROM ticks_nsefut_zip_lcl t WHERE DATE(time) = '{dfDates.iloc[x]['date']}';"
    df = pd.read_sql(text(sql), dbConn)
    symlist = df.symbol.unique()

    f = BASE_PATH + str(dfDates.iloc[x]['date']) + ' ( Symbols ' + str(
        len(symlist)) + ' - Rows ' + str(len(df)) + ' ).csv'
    df["volume"] = ""
    df["buy_demand"] = ""
    df["sell_demand"] = ""
    df["open_interest"] = ""
    df.to_csv(f, index=False, columns=header_list)
