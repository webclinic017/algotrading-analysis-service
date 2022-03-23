from numpy import double
from App.Services.Instruments import LoadInstruments
import pandas as pd


def execute(dbConn, sid):

    if (sid == 'instruments'):
        results = LoadInstruments(dbConn)
    else:
        return 'No Service Found'
