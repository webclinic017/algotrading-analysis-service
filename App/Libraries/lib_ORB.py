def getORB(Xdf, Xcandles):
    ORBdf = Xdf.iloc[0:Xcandles]
    return ORBdf["Low"].min(), ORBdf["High"].max(), \
             Xdf["Low"].min(),   Xdf["High"].max()