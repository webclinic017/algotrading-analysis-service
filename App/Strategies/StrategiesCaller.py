from App.Strategies.S01_ORB import S01_ORB_Force
import pandas as pd



def callStrategies():

    results = pd.DataFrame()
    print('callStrategies')
    S01_ORB_Force("filteredDayDF", "selectedDate", results)

