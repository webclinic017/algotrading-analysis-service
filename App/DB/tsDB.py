import os
import json
from pgcopy.copy import null
import psycopg2
import sqlalchemy
import pandas as pd
from pandas.io.json import json_normalize
import App.Libraries.lib_results as res


def dbConnect():  # connect to database

    fileDir = os.path.dirname(os.path.realpath(__file__))
    credentials_file = os.path.join(fileDir, "./../../credentials.json")

    f = open(credentials_file, "r")
    credentials = json.load(f)
    f.close()

    db_url = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
        database=credentials["DB_NAME"],
        host=credentials["DB_HOST"],
        user=credentials["DB_USER"],
        password=credentials["DB_PASS"],
        port=credentials["DB_PORT"])

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
    sql = f"select * from strategies where strategy_id = '{cellValue}' "
    df = pd.read_sql(sql, conn)
    df.to_dict('records')
    return df


def fetchCandlesBetween(conn, symbol, sdatetime, edatetime, candleSize):
    sql = f"select * FROM candles_{candleSize}min WHERE (candle between '{sdatetime}' and '{edatetime}') and symbol like '%%{symbol}%%' ORDER by candle asc"
    return pd.read_sql(sql, conn)


def fetchCandlesOnDate(conn, symbol, date, candleSize):
    sql = f"SELECT * FROM candles_{candleSize}min WHERE symbol LIKE '%%{symbol}%%' AND DATE_TRUNC('day', candle) = '{date}' ORDER BY candle DESC"
    return pd.read_sql(sql, conn)


def saveTradeSignalsToDB(conn, df):
    df.to_sql('signals_trading', conn, if_exists='append', index=False)


def createAllTables(conn):
    if (db_table_exists(conn, "signals_trading")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE signals_trading (
            s_order_id SERIAL PRIMARY KEY NOT NULL,

            strategy_id  VARCHAR(50) NOT NULL,
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
        conn.execute(tradingSignalsTblQuery)

    if (db_table_exists(conn, "signals_simulation")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE signals_simulation (
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
        conn.execute(tradingSignalsTblQuery)

    if (db_table_exists(conn, "algotrading_status")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE algotrading_status (
                status VARCHAR(50) NOT NULL,
                processing_strategy_id INTEGER,
                processing_simulation_id INTEGER,
                processing_percentage SMALLINT
            );"""
        conn.execute(tradingSignalsTblQuery)

    if (db_table_exists(conn, "strategies")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE strategies (
                strategy_id VARCHAR(30) UNIQUE NOT NULL,
                strategy_en BOOLEAN NOT NULL DEFAULT 'false',
                p_engine  VARCHAR(50) NOT NULL,
                p_trigger_time TIME NOT NULL,
                p_trigger_days VARCHAR(50) NOT NULL,
                p_target_per SMALLINT NOT NULL,
                p_candle_size SMALLINT NOT NULL,
                p_stoploss_per SMALLINT NOT NULL,
                p_deep_stoploss_per SMALLINT NOT NULL,
                p_delayed_stopLoss_min TIME NOT NULL,
                p_stall_detect_period_min TIME NOT NULL,
                p_trail_target_en BOOLEAN NOT NULL,
                p_position_reversal_en BOOLEAN NOT NULL                
            );"""
        conn.execute(tradingSignalsTblQuery)
