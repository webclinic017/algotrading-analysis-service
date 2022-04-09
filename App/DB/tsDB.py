import os
import json
import psycopg2
import sqlalchemy
import pandas as pd
import datetime
from os.path import exists
from pandas.io.json import json_normalize
import App.Libraries.lib_results as res


def dbConnect():  # connect to database

    fileDir = os.path.dirname(os.path.realpath(__file__))
    credentials_file = os.path.join(fileDir, "./../../credentials.json")

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

    else:
        db_url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
            database=os.getenv('DB_NAME'),
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            port=os.getenv('DB_PORT'))

    engine = sqlalchemy.create_engine(db_url)
    return engine


def db_table_exists(conn, tablename):
    # thanks to Peter Hansen's answer for this sql

    sql = f"select * from information_schema.tables where table_name='{tablename}'"

    # return results of sql query from conn as a pandas dataframe
    results_df = pd.read_sql_query(sql, conn)

    # True if we got any results back, False if we didn't
    return bool(len(results_df))


def readAlgoParamsJson(conn, cellValue):
    sql = f"select * from strategies where strategy = '{cellValue}' "
    df = pd.read_sql(sql, conn)
    df2 = json_normalize(df.iloc[0]['controls'])
    df_merged = pd.concat([df, df2], axis=1)
    df_merged.to_dict('records')
    return df_merged


def fetchCandlesBetweenMultiSymbol(conn, symbol, sdatetime, edatetime,
                                   candleSize):
    sql = f"select * FROM candles_{candleSize}min WHERE (candle between '{sdatetime}' and '{edatetime}') and symbol like '%%{symbol}%%' ORDER by candle asc"
    return pd.read_sql(sql, conn)


def fetchCandlesBetweenSingleSymbol(conn, symbol, sdatetime, edatetime,
                                    candleSize):
    sql = f"select * FROM candles_{candleSize}min WHERE (candle between '{sdatetime}' and '{edatetime}') and symbol like '{symbol}' ORDER by candle asc"
    return pd.read_sql(sql, conn)


def fetchCandlesOnDate(conn, symbol, date, candleSize):
    sql = f"SELECT * FROM candles_{candleSize}min WHERE symbol LIKE '%%{symbol}%%' AND DATE_TRUNC('day', candle) = '{date}' ORDER BY candle DESC"
    return pd.read_sql(sql, conn)


def fetchTicksData(conn, current_date):
    sql = f"SELECT  * FROM ticks_stk WHERE CAST(time AS date) = '{current_date}' UNION ALL SELECT * FROM ticks_nsefut WHERE CAST(time AS date) = '{current_date}'"
    df = pd.read_sql(sql, conn)
    return df


def saveCandles(conn, df):
    df.to_sql('candles_1min', conn, if_exists='append')


def saveTradeSignalsToDB(conn, df):
    df.to_sql('signals_trading', conn, if_exists='append', index=False)


# drop table if exists, then create table and insert data
def saveInstrumentsToDB(conn, df):
    if (db_table_exists(conn, "instruments")) == True:
        sql = f"DROP TABLE instruments"
        conn.execute(sql)

    sqlQuery = """CREATE TABLE instruments (
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
    df.to_sql('instruments', conn, if_exists='replace', index=False)


def saveDataFrameToDB(conn, df):
    df.to_sql('instruments', conn, if_exists='append', index=False)


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
            SELECT set_chunk_time_interval('candles_1min', INTERVAL '1 months');"""
        conn.execute(sqlQuery)

    if (db_table_exists(conn, "signals_trading")) == False:
        # create table
        sqlQuery = """CREATE TABLE signals_trading (
            id SERIAL PRIMARY KEY NOT NULL,
            date DATE NOT NULL,
            instr TEXT NOT NULL,
            strategy  VARCHAR(100) NOT NULL,
            dir VARCHAR(50) NOT NULL,
            entry DOUBLE PRECISION DEFAULT 0.0,
            entry_time TIME DEFAULT '00:00:00',
            target DOUBLE PRECISION NOT NULL,
            stoploss DOUBLE PRECISION NOT NULL,
            trade_id INTEGER DEFAULT 0,
            exit_val DOUBLE PRECISION DEFAULT 0.0,
            exit_time TIME DEFAULT '00:00:00',
            exit_reason TEXT  DEFAULT 'NA',
            swing_min DOUBLE PRECISION DEFAULT 0.0,
            swing_max DOUBLE PRECISION DEFAULT 0.0,
            swing_min_time TIME DEFAULT '00:00:00',
            swing_max_time TIME DEFAULT '00:00:00'
        );"""
        conn.execute(sqlQuery)

    if (db_table_exists(conn, "signals_simulation")) == False:
        # create table
        sqlQuery = """CREATE TABLE signals_simulation (
            s_order_id SERIAL PRIMARY KEY NOT NULL,
            strategy_id  VARCHAR(50) NOT NULL,
            simulation_id INTEGER,
            
            s_date DATE NOT NULL,
            s_direction VARCHAR(50) NOT NULL,
            t_entry DOUBLE PRECISION NOT NULL,
            t_entry_time TIME NOT NULL,
            s_target DOUBLE PRECISION NOT NULL,
            s_stoploss DOUBLE PRECISION NOT NULL,
            t_trade_confirmed_en BOOLEAN,
            s_instr_token VARCHAR(200),

            r_exit_val DOUBLE PRECISION,
            r_exit_time TIME,
            r_exit_reason VARCHAR(100),

            r_swing_min DOUBLE PRECISION,
            r_swing_max DOUBLE PRECISION,
            r_swing_min_time TIME,
            r_swing_max_time TIME

        );"""
        conn.execute(sqlQuery)

    if (db_table_exists(conn, "strategies")) == False:
        # create table
        sqlQuery = """CREATE TABLE strategies (
                strategy VARCHAR(100) UNIQUE NOT NULL,
                enabled BOOLEAN NOT NULL DEFAULT 'false',
                engine  VARCHAR(50) NOT NULL,
                trigger_time TIME NOT NULL,
                trigger_days VARCHAR(100) NOT NULL,
                cdl_size SMALLINT NOT NULL,
                instruments TEXT,
                controls JSON
            );"""
        conn.execute(sqlQuery)
