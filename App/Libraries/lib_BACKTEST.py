
def btEngine():
    return 0


def btResultsParser(data, fltr):
    
    # round digits
    data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']] = \
    data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']].astype(float).round(1)
    
    print('Results: ', data['Result'].sum().astype(float).round(1))
    print(data['Reason'].value_counts())
    print(data['Signal'].value_counts())
    
    # store to csv file
    data.to_csv('./Results/BT_'+fltr+'_ORB-Force.csv', index=False)  
