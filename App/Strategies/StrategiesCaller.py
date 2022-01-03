from App.Strategies.S01_ORB import S01_ORB_Force
import pandas as pd



def execute(algo):

    results = pd.DataFrame()
    if (algo == 'S01_ORB'):
        results = S01_ORB_Force("filteredDayDF", "selectedDate", results)
    else:
        return 'No Algo Found'

