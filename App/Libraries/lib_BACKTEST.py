def btResultsParser(data, fltr, debug_image):

    # round digits
    # data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']] = \
    # data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']].astype(float).round(1)

    # print('Results: ', data['Result'].sum().astype(float).round(1))
    print(data['dir'].value_counts())
    # print(data['Signal'].value_counts())

    # store to csv file
    # data.to_csv('./Results/BT_' + fltr + '_ORB-Force.csv', index=False)


#  todo: create image for every scan using parser