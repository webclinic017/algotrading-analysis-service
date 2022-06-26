import datetime
from dateutil.relativedelta import relativedelta


def getORB(Xdf):
    ORBdf = Xdf.between_time('09:15', '09:30')
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
