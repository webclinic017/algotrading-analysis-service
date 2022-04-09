from numpy import double
from App.Services.CreateCandles import CreateCandlesInDb
from App.Services.Instruments import LoadInstruments
import pandas as pd


def execute(dbConn, sid, date):

    if (sid == 'instruments'):
        results = LoadInstruments(dbConn)
    elif (sid == 'createCandles'):
        results = CreateCandlesInDb(dbConn, date, '1T')
    else:
        return 'No Service Found'
