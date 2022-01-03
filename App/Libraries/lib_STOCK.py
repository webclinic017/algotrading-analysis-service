SUB_PATH = '/Data/Consolidated/'

import pandas as pd
from glob import iglob

def readStockData(path, fltr, nifty):
    header_list = ['Date', 'DateStr','TimeStr' ,\
                   'Open', 'High', 'Low', 'Close', \
                   'Null1', 'Null2', 'Null3', 'Null4']
    
    path = path + SUB_PATH + fltr + '*' + nifty + '.txt'
    
    df = pd.concat((pd.read_csv(f, header=None, sep=',', names=header_list)\
                    for f in iglob(path, recursive=True)), ignore_index=True)
    
    df['Date']=(pd.to_datetime(df.DateStr.astype(str) + ' ' + \
                               df.TimeStr.astype(str), format='%Y%m%d %H:%M'))
    
    df_ = df.drop(['DateStr', 'TimeStr', 'Null1', 'Null2', 'Null3', 'Null4'], axis=1)
    df_.set_index('Date',inplace=True)
    
    # List all the dates into new DF
    df_dates_ = pd.DataFrame(index=df_.index)
    df_dates_.index = df_dates_.index.date
    # drop_duplicates - does not work on datetimeindex index
    df_dates_ = df_dates_[~df_dates_.index.duplicated()]   

    print('Total Entries: ',len(df_), \
          "\nDays: ", df_.index.max() - df_.index.min(), \
         '\nReading Stock Data:\n', path)
    
    return df_, df_dates_