import datetime
from dateutil.relativedelta import relativedelta


def res_exit(df, i, r, er):
    df.at[0, "exit_time"] = i
    df.at[0, "exit"] = r["close"]
    df.at[0, "exit_reason"] = er
    df.at[0, "status"] = "signal-processed"
    return df


def eod(df, r):

    if r.at[0, "exit_reason"] == "":

        eod_cdls = df.between_time("15:16", "15:30")

        if len(eod_cdls):
            row = eod_cdls.iloc[0]
            r.at[0, "exit_time"] = 0
            r.at[0, "exit"] = row["close"]
            r.at[0, "exit_reason"] = "eod"
            r.at[0, "status"] = "signal-processed"

    return r


def getORB(Xdf):
    ORBdf = Xdf.between_time("09:15", "09:30")
    return ORBdf["low"].min(), ORBdf["high"].max()


def getDates(duration, end_date):

    base = duration.split(" ")
    numPart = int(base[0])
    unit = base[1]

    if end_date == "" or end_date is None:
        end = datetime.date.today()
    else:
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    if unit == "day" or unit == "days":
        start = end - relativedelta(days=numPart)
    elif unit == "week" or unit == "weeks":
        start = end - relativedelta(weeks=numPart)
    elif unit == "mon" or unit == "month" or unit == "months":
        start = end - relativedelta(months=numPart)
    elif unit == "year" or unit == "years":
        start = end - relativedelta(years=numPart)
    else:
        print("Invalid duration")

    return start, end
