import os
import sys
import time
import numpy as np
import pandas as pd
# from tqdm import tqdm
# from time import strftime
# import matplotlib.pyplot as plt

from App.DB import tsDB
import datetime
import pandas as pd

dbConn = tsDB.dbConnect()

import pandas as pd
import glob

header_list = [
    'time', 'symbol', 'last_traded_price', 'buy_demand', 'sell_demand',
    'trades_till_now', 'open_interest'
]

BASE_PATH = "/home/parag/devArea/algotrading-analysis-service/"
SUB_PATH = 'Data/ticks_nsestk/'
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
    df.to_sql('ticks_nsestk_lcl', dbConn, if_exists='append', index=False)

SUB_PATH = 'Data/ticks_nsefut/'
path = BASE_PATH + SUB_PATH + '*.csv'
cnt = 0

for filename in glob.glob(path):
    cnt = cnt + 1
    df = pd.read_csv(
        filename,
        sep=',',
        header=0,
    )
    print(str(++cnt), filename + ' len:' + str(len(df)))
    df.to_sql('ticks_nsefut_lcl', dbConn, if_exists='append', index=False)
