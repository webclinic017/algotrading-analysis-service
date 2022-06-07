def getORB(Xdf):
    ORBdf = Xdf.between_time('09:15', '09:30')
    return ORBdf["low"].min(), ORBdf["high"].max()