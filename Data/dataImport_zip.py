import os
import sys
import time
import numpy as np
import pandas as pd
from pathlib import Path

from App.DB import tsDB
import datetime
import pandas as pd

dbConn = tsDB.dbConnect()

import pandas as pd
import glob

header_list = [
    'tim', 'symbol', 'last_traded_price', 'buy_demand', 'sell_demand',
    'trades_till_now', 'open_interest'
]

header_list_zipfile_data = [
    'symbol',
    'date',
    'time',
    'open',
    'high',
    'low',
    'close',
]

BASE_PATH = "/home/parag/devArea/algotrading-analysis-service/"
SUB_PATH = 'Data/Consolidated/'

path = BASE_PATH + SUB_PATH + '*.txt'
cnt = 0

for filename in glob.glob(path):
    # print(filename)
    cnt = cnt + 1
    df = pd.read_csv(
        filename,
        sep=',',
        header=None,
    )
    # print(df.head(2))
    if len(df.columns) == 9:
        df.drop(df.columns[7], axis=1, inplace=True)
        df.drop(df.columns[7], axis=1, inplace=True)
        df.columns = header_list_zipfile_data
    elif len(df.columns) == 8:
        df.drop(df.columns[7], axis=1, inplace=True)
        df.columns = header_list_zipfile_data
    else:
        df.columns = header_list_zipfile_data

    df['time']=(pd.to_datetime(df.date.astype(str) + ' ' + \
                               df.time.astype(str), format='%Y%m%d %H:%M'))
    df.drop(['date'], axis=1, inplace=True)

    # print(df.head(3))

    print(str(++cnt), filename + ' len:' + str(len(df)))
    df.to_sql('ticks_nsefut_zip_lcl', dbConn, if_exists='append', index=False)
