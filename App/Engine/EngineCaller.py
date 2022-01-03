from App.Engine.E01_Intraday_Trading_Engine import IntraDay_Directional_NakedPosition
import pandas as pd



def execute(algo):

    results = pd.DataFrame()
    if (algo == 'S01_ORB'):
        results = IntraDay_Directional_NakedPosition("dayDF", "selectedDate", "strategy")
    else:
        return 'No Algo Found'

