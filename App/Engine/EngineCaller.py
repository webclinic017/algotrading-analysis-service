from numpy import double
from App.Engine.E01_Intraday_Trading_Engine import IntraDay_Directional_NakedPosition
import pandas as pd

def execute(algo):

    results = pd.DataFrame()
    
    # TODO:
    # 1. Read the signal DB 
    # 2. For each signal, call the algo
    # 3. For each algo, call the engine
    # 4. For each engine, call the backtest
    # 5. For each backtest, call the results parser
    



    if (algo == 'IntraDay'):
        results = IntraDay_Directional_NakedPosition("dayDF", "selectedDate", "strategy")
    else:
        return 'No Algo Found'

