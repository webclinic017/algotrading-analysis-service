import os
import glob
import json
import sqlalchemy
import numpy as np
import pandas as pd
from sqlalchemy import text
from os.path import exists

BASE_PATH = "/home/parag/devArea/algotrading-analysis-service/Data/"
TABLE = 'candles_1min'

header_list = [
    'time',
    'symbol',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'buy_demand',
    'sell_demand',
    'open_interest',
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

folders = ["1min_nsefut_zip/", "1min_nsefut/", "1min_nsestk/"]

for x in folders:
    SUB_PATH = x
    path = BASE_PATH + SUB_PATH + '*.csv'
    cnt = 0

    for filename in glob.glob(path):
        cnt = cnt + 1
        df = pd.read_csv(
            filename,
            sep=',',
            header=0,
        )
        print(str(cnt), filename + ' len:' + str(len(df)))
        df.to_sql(TABLE, dbConn, if_exists='append', index=False)
