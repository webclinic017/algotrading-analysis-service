import sqlalchemy
from sqlalchemy import text
import pandas as pd
from datetime import datetime
import App.Libraries.lib_CANDLES as libC
from os.path import exists
import os
import json
import numpy as np


def envVar():

    dict = {}

    fileDir = os.path.dirname(os.path.realpath(__file__))
    credentials_file = os.path.join(fileDir, "./../../credentials.json")

    if exists(credentials_file):
        f = open(credentials_file, "r")
        credentials = json.load(f)
        f.close()
        dict['charting_sw'] = credentials['CHARTING_SW']
        dict['database'] = credentials[credentials['DB_PROFILE']]['NAME']
        dict['host'] = credentials[credentials['DB_PROFILE']]['ADDRESS']
        dict['user'] = credentials[credentials['DB_PROFILE']]['USERNAME']
        dict['password'] = credentials[credentials['DB_PROFILE']]['PASSWORD']
        dict['port'] = credentials[credentials['DB_PROFILE']]['PORT']

        if credentials['TEST_MODE'] == True:
            dict['tst'] = credentials['DB_TABLES']['TEST_POSTFIX']
        else:
            dict['tst'] = ""

        dict['upre'] = credentials['DB_TABLES']['PREFIX_USER_ID']
        dict['tbl_instruments'] = credentials['DB_TABLES']['INSTRUMENTS']
        dict['tbl_tick_nsefut'] = credentials['DB_TABLES']['TICK_NSEFUT']
        dict['tbl_tick_nsestk'] = credentials['DB_TABLES']['TICK_NSESTK']
        dict['tbl_user_setting'] = credentials['DB_TABLES']['USER_SETTING']
        dict['tbl_user_symbols'] = credentials['DB_TABLES']['USER_SYMBOLS']
        dict['tbl_orderbook'] = credentials['DB_TABLES']['ORDER_BOOK']
        dict['tbl_usr_strategies'] = credentials['DB_TABLES'][
            'USER_STRATEGIES']

    else:
        dict['database'] = os.getenv('TIMESCALEDB_NAME'),
        dict['host'] = os.getenv('TIMESCALEDB_ADDRESS'),
        dict['user'] = os.getenv('TIMESCALEDB_USER'),
        dict['password'] = os.getenv('TIMESCALEDB_PASSWORD'),
        dict['port'] = os.getenv('TIMESCALEDB_PORT')

        if os.getenv('TEST_MODE') == True:
            dict['tst'] = os.getenv('DB_TEST_POSTFIX')
        else:
            dict['tst'] = ""

        dict['upre'] = os.getenv('DB_TBL_PREFIX_USER_ID')
        dict['tbl_instruments'] = os.getenv('DB_TBL_INSTRUMENTS')
        dict['tbl_tick_nsefut'] = os.getenv('DB_TBL_TICK_NSEFUT')
        dict['tbl_tick_nsestk'] = os.getenv('DB_TBL_TICK_NSESTK')
        dict['tbl_user_setting'] = os.getenv('DB_TBL_USER_SETTING')
        dict['tbl_user_symbols'] = os.getenv('DB_TBL_USER_SYMBOLS')
        dict['tbl_orderbook'] = os.getenv('DB_TBL_ORDER_BOOK')
        dict['tbl_usr_strategies'] = os.getenv('DB_TBL_USER_STRATEGIES')


# Update Table Names ------------------
    dict['tbl_tick_nsefut'] = dict['tbl_tick_nsefut'] + dict['tst']
    dict['tbl_tick_nsestk'] = dict['tbl_tick_nsestk'] + dict['tst']

    # Tables with user id + test name
    dict['tbl_user_setting'] = dict['upre'] + dict['tbl_user_setting'] + dict[
        'tst']
    dict['tbl_user_symbols'] = dict['upre'] + dict['tbl_user_symbols'] + dict[
        'tst']
    dict['tbl_usr_strategies'] = dict['upre'] + dict[
        'tbl_usr_strategies'] + dict['tst']
    dict['tbl_orderbook'] = dict['upre'] + dict['tbl_orderbook'] + dict['tst']

    return dict


def dbConnect(env):  # connect to database

    db_url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
        database=env['database'],
        host=env['host'],
        user=env['user'],
        password=env['password'],
        port=env['port'])

    return sqlalchemy.create_engine(db_url)


def get_dates_list(conn, date_start, date_end):
    sql = f"SELECT DISTINCT DATE_TRUNC('day', time) AS dates FROM candles_1min WHERE CAST(time AS date) BETWEEN '{date_start}' AND '{date_end}' ORDER BY dates DESC"

    if date_start == "" or date_end == "":
        sql = f"SELECT DISTINCT DATE_TRUNC('day', time) AS dates FROM candles_1min ORDER BY dates DESC"

    df = pd.read_sql(text(sql), conn)
    return df['dates'].astype(str).tolist()


def db_table_exists(conn, tablename):
    # thanks to Peter Hansen's answer for this sql

    sql = f"select * from information_schema.tables where table_name='{tablename}'"

    # return results of sql query from conn as a pandas dataframe
    results_df = pd.read_sql_query(sql, conn)

    # True if we got any results back, False if we didn't
    return bool(len(results_df))


def readAlgoParams(env, conn, cellValue):

    try:
        sql = f"SELECT parameters FROM  {env['tbl_usr_strategies']} WHERE  strategy LIKE '{cellValue}%';"
        ap = pd.read_sql(text(sql), conn)
        if len(ap) == 0:
            return None

        ap1 = ap.to_records(index=False)
        ap2 = ap1[0]['parameters']

        # convert to floats
        ap2['controls']['target_per'] = float(ap2['controls']['target_per'] /
                                              100)

        ap2['controls']['stoploss_per'] = float(
            ap2['controls']['stoploss_per'] / 100)

        ap2['controls']['budget_max_per'] = float(
            ap2['controls']['budget_max_per'] / 100)

    except Exception as e:
        print('tsDb.py - Read error for ', e)
        return None

    return ap2


def getCdlBtwnTime(env, conn, symbol, date, timeRange, candleSize):
    # print(datetime.today().date())
    df = pd.DataFrame()

    if "NaT" in date:
        return pd.DataFrame()

    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    # print(date_time_obj.date())

    startDT = date + ' ' + timeRange[0]
    endDT = date + ' ' + timeRange[1]

    if date_time_obj.date() == datetime.today().date():
        sql = f"SELECT * FROM {env['tbl_tick_nsestk']} WHERE ((time BETWEEN '{startDT}' AND '{endDT}') AND symbol LIKE '%{symbol}%') UNION ALL SELECT * FROM {env['tbl_tick_nsefut']} WHERE ((time BETWEEN '{startDT}' AND '{endDT}')  AND symbol LIKE '%{symbol}%')"
        df = pd.read_sql(text(sql), conn)
        df = libC.TickToCdl(df, date, str(candleSize) + "T")

    else:
        sql = f"SELECT * FROM candles_1min cm WHERE (time BETWEEN '{startDT}' AND '{endDT}') AND symbol LIKE '%{symbol}%' ORDER by time ASC;"
        df = pd.read_sql(text(sql), conn)
        df = libC.CdlConv(df, candleSize + "T")

    # print(df.head(30))

    return df


def fetchCandlesOnDate(conn, symbol, date, candleSize):
    sql = f"SELECT * FROM candles_{candleSize}min WHERE symbol LIKE '%%{symbol}%%' AND DATE_TRUNC('day', candle) = '{date}' ORDER BY candle DESC"
    return pd.read_sql(text(sql), conn)


def fetchTicksData(env, conn, current_date):
    sql = f"SELECT  * FROM {env['tbl_tick_nsestk']} WHERE CAST(time AS date) = '{current_date}' UNION ALL SELECT * FROM {env['tbl_tick_nsefut']} WHERE CAST(time AS date) = '{current_date}'"
    df = pd.read_sql(sql, conn)
    return df


def fetchTicks(conn, current_date, table):
    sql = f"SELECT * FROM {table} WHERE CAST(time AS date) = '{current_date}'"
    df = pd.read_sql(sql, conn)
    return df


def updateTable(conn, table, df):
    df.to_sql(table, conn, if_exists='append')


# drop table if exists, then create table and insert data
def saveInstrumentsToDB(env, conn, df):
    if (db_table_exists(conn, env['tbl_instruments'])) == True:
        sql = f"DROP TABLE {env['tbl_instruments']};"
        conn.execute(sql)

    sqlQuery = """CREATE TABLE """ + env['tbl_instruments'] + """ (
                        instrument_token INTEGER NOT NULL,
                        exchange_token INTEGER NOT NULL,
                        tradingsymbol TEXT NOT NULL,
                        "name" TEXT NULL,
                        last_price DOUBLE PRECISION NULL DEFAULT 0,
                        expiry DATE NULL,
                        strike DOUBLE PRECISION NULL,
                        tick_size DOUBLE PRECISION NULL,
                        lot_size INTEGER NULL,
                        instrument_type VARCHAR(10) NULL,
                        segment VARCHAR(10) NULL,
                        exchange VARCHAR(10) NULL
                    );"""
    conn.execute(sqlQuery)
    df.to_sql(env['tbl_instruments'], conn, if_exists='replace', index=False)


def createAllTables(conn):

    if (db_table_exists(conn, "candles_1min")) == False:
        # create table
        sqlQuery = """CREATE TABLE candles_1min (
            time TIMESTAMP NOT NULL,
            symbol TEXT NOT NULL,
            open DOUBLE PRECISION,
            high DOUBLE PRECISION,
            low DOUBLE PRECISION,
            close DOUBLE PRECISION,
            volume INTEGER DEFAULT 0,
            buy_demand INTEGER DEFAULT 0,
            sell_demand INTEGER DEFAULT 0,
            open_interest INTEGER DEFAULT 0
            );
            SELECT create_hypertable('candles_1min', 'time');
            SELECT set_chunk_time_interval('candles_1min', INTERVAL '1 months');
            """
        conn.execute(sqlQuery)
