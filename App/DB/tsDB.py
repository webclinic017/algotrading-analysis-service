import os
import json
from pgcopy.copy import null
import psycopg2
import pandas as pd
from pandas.io.json import json_normalize


def dbConnect():  # connect to database

    fileDir = os.path.dirname(os.path.realpath(__file__))
    credentials_file = os.path.join(fileDir, "./../../credentials.json")

    f = open(credentials_file, "r")
    credentials = json.load(f)
    f.close()

    conn = psycopg2.connect(
        database=credentials["DB_NAME"],
        host=credentials["DB_HOST"],
        user=credentials["DB_USER"],
        password=credentials["DB_PASS"],
        port=credentials["DB_PORT"],
    )
    return conn


def db_table_exists(conn, tablename):
    # thanks to Peter Hansen's answer for this sql
    sql = f"select * from information_schema.tables where table_name='{tablename}'"

    # return results of sql query from conn as a pandas dataframe
    results_df = pd.read_sql_query(sql, conn)

    # True if we got any results back, False if we didn't
    return bool(len(results_df))


def readAlgoParams(conn, cellValue):
    # read all rows from table
    cur = conn.cursor()
    cur.execute(
        f"select * from algotrading_strategy_params where strategy_id = '{cellValue}' "
    )
    rows = cur.fetchone()
    cur.close()
    return rows


def fetchCandlesOnDate(conn, symbol, date, candleSize):
    # read all rows from table
    sql = f"SELECT * FROM candles_{candleSize}min WHERE symbol LIKE '%{symbol}%' AND DATE_TRUNC('day', bucket) = '{date}' ORDER BY bucket DESC"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return rows


def fetchCandlesBetweenTime(conn, symbol, timeFrom, timeTill, candleSize):
    # read all rows from table
    sql = f"SELECT * FROM candles_{candleSize}min WHERE symbol LIKE '%{symbol}%' AND bucket BETWEEN '{timeFrom}' and '{timeTill}'ORDER BY bucket DESC"
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return rows


def createAllTables(conn):
    if (db_table_exists(conn, "algotrading_signals_trading")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE algotrading_signals_trading (
            strategy_id  VARCHAR(10) NOT NULL,

            s_order_id SERIAL UNIQUE NOT NULL,
            s_date DATE NOT NULL,
            s_direction VARCHAR(50) NOT NULL,
            t_entry DOUBLE PRECISION NOT NULL,
            t_entry_time TIMESTAMP NOT NULL,
            s_target DOUBLE PRECISION NOT NULL,
            s_stoploss DOUBLE PRECISION NOT NULL,
            t_trade_confirmed_en BOOLEAN,
            s_instr_token INTEGER,

            r_exit_val DOUBLE PRECISION,
            r_exit_time TIME,
            r_exit_reason VARCHAR(100),

            r_swing_min DOUBLE PRECISION,
            r_swing_max DOUBLE PRECISION,
            r_swing_min_time TIME,
            r_swing_max_time TIME
        );"""
        cur = conn.cursor()
        cur.execute(tradingSignalsTblQuery)
        conn.commit()
        cur.close()

    if (db_table_exists(conn, "algotrading_signals_simulation")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE algotrading_signals_simulation (
            strategy_id  VARCHAR(10) NOT NULL,
            simulation_id INTEGER NOT NULL,

            s_order_id SERIAL UNIQUE NOT NULL,
            s_date DATE NOT NULL,
            s_direction VARCHAR(50) NOT NULL,
            t_entry DOUBLE PRECISION NOT NULL,
            t_entry_time TIMESTAMP NOT NULL,
            s_target DOUBLE PRECISION NOT NULL,
            s_stoploss DOUBLE PRECISION NOT NULL,
            t_trade_confirmed_en BOOLEAN,
            s_instr_token INTEGER,

            r_exit_val DOUBLE PRECISION,
            r_exit_time TIME,
            r_exit_reason VARCHAR(100),

            r_swing_min DOUBLE PRECISION,
            r_swing_max DOUBLE PRECISION,
            r_swing_min_time TIME,
            r_swing_max_time TIME

        );"""
        cur = conn.cursor()
        cur.execute(tradingSignalsTblQuery)
        conn.commit()
        cur.close()

    if (db_table_exists(conn, "algotrading_analysis_service_status")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE algotrading_analysis_service_status (
                status VARCHAR(50) NOT NULL,
                processing_strategy_id INTEGER,
                processing_simulation_id INTEGER,
                processing_percentage SMALLINT
            );"""
        cur = conn.cursor()
        cur.execute(tradingSignalsTblQuery)
        conn.commit()
        cur.close()

    if (db_table_exists(conn, "algotrading_strategy_params")) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE algotrading_strategy_params (
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
        cur = conn.cursor()
        cur.execute(tradingSignalsTblQuery)
        conn.commit()
        cur.close()
