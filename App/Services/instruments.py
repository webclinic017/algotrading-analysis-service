import io
import requests
import pandas as pd
import App.DB.tsDB as db
from time import strftime


def LoadInstruments(env, dbConn):

    instrumentsUrl = "http://api.kite.trade/instruments"
    instruments = requests.get(instrumentsUrl).content
    instrDF = pd.read_csv(io.StringIO(instruments.decode('utf-8')))

    db.saveInstrumentsToDB(env, dbConn, instrDF)
