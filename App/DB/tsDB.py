import os
import json
import psycopg2
import datetime
import pandas as pd
from pgcopy import CopyManager
from pandas.io.json import json_normalize


COLUMNS = ('time', 'symbol', 'last_price', 'open', 'close', 'low', 'high', 'volume')


def dbConnect():  # connect to database

    fileDir = os.path.dirname(os.path.realpath(__file__))
    credentials_file = os.path.join(fileDir, './../../credentials.json')

    f = open(credentials_file, "r")
    credentials = json.load(f)
    f.close()

    conn = psycopg2.connect(database=credentials["DB_NAME"],
                        host=credentials["DB_HOST"],
                        user=credentials["DB_USER"],
                        password=credentials["DB_PASS"],
                        port=credentials["DB_PORT"])
    return conn


def db_table_exists(conn, tablename):
    # thanks to Peter Hansen's answer for this sql
    sql = f"select * from information_schema.tables where table_name='{tablename}'" 
    
    # return results of sql query from conn as a pandas dataframe
    results_df = pd.read_sql_query(sql, conn)

    # True if we got any results back, False if we didn't
    return bool(len(results_df))


def createAllTables(conn):
    if (db_table_exists(conn, 'signals_trading' )) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE signals_trading (
            order_id SERIAL UNIQUE NOT NULL,
            Strategy  VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            candle_size SMALLINT NOT NULL,
            signal VARCHAR(50) NOT NULL,
            entry DOUBLE PRECISION NOT NULL,
            entry_time TIMESTAMP NOT NULL,
            target DOUBLE PRECISION NOT NULL,
            stoploss DOUBLE PRECISION NOT NULL,

            trade_confirmed_en BOOLEAN,
            instr_token INTEGER,
            stoploss_per SMALLINT NOT NULL,
            deep_stoploss_per SMALLINT NOT NULL,
            delayed_stopLoss_min TIME NOT NULL,
            stall_detect_period_min TIME NOT NULL,
            trail_target_en BOOLEAN NOT NULL,
            position_reversal_en BOOLEAN NOT NULL,

            exit_val DOUBLE PRECISION,
            exit_time TIME,
            exit_reason VARCHAR(100),

            swing_min DOUBLE PRECISION,
            swing_max DOUBLE PRECISION,
            swing_min_time TIME,
            swing_max_time TIME
        );"""
        cur = conn.cursor()
        cur.execute(tradingSignalsTblQuery)
        conn.commit()
        cur.close()

    if (db_table_exists(conn, 'signals_simulation' )) == False:
        # create table
        tradingSignalsTblQuery = """CREATE TABLE signals_simulation (
            simulation_id INTEGER NOT NULL,

            order_id SERIAL UNIQUE NOT NULL,
            Strategy  VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            candle_size SMALLINT NOT NULL,
            signal VARCHAR(50) NOT NULL,
            entry DOUBLE PRECISION NOT NULL,
            entry_time TIMESTAMP NOT NULL,
            target DOUBLE PRECISION NOT NULL,
            stoploss DOUBLE PRECISION NOT NULL,

            instr_token INTEGER,
            stoploss_per SMALLINT NOT NULL,
            deep_stoploss_per SMALLINT NOT NULL,
            delayed_stopLoss_min TIME NOT NULL,
            stall_detect_period_min TIME NOT NULL,
            trail_target_en BOOLEAN NOT NULL,
            position_reversal_en BOOLEAN NOT NULL,

            exit_val DOUBLE PRECISION,
            exit_time TIME,
            exit_reason VARCHAR(100),

            swing_min DOUBLE PRECISION,
            swing_max DOUBLE PRECISION,
            swing_min_time TIME,
            swing_max_time TIME
        );"""
        cur = conn.cursor()
        cur.execute(tradingSignalsTblQuery)
        conn.commit()
        cur.close()

    if (db_table_exists(conn, 'algotrading_analysis_service_status' )) == False:
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


