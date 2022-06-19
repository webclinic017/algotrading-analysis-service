import pandas as pd
from fpdf import FPDF
from datetime import datetime


def btResultsParser(data, algo, plot, duration):

    generate_stock_report

    # round digits
    # data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']] = \
    # data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']].astype(float).round(1)

    # print('Results: ', data['Result'].sum().astype(float).round(1))
    print(data["dir"].value_counts())
    # print(data['Signal'].value_counts())
    # print(data["time"].dt.strftime("%Y-%m-%d %H:%M:%S"))

    # store to csv file
    BASE_PATH = "/home/parag/devArea/algotrading-analysis-service/StudyZone/results/"

    dt = datetime.now().strftime("%Y-%m-%dT%H%M%S")
    f = BASE_PATH + dt + "-" + algo + "-" + duration + ".csv"
    data.to_csv(f, index=False)

    from fpdf import FPDF

    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font("Arial", "B", 16)
    # pdf.cell(40, 10, "Hello World!")
    # pdf.output("tuto1.pdf", "F")


#  todo: create image for every scan using parser


def generate_stock_report():

    df = pd.read_csv(
        "/home/parag/devArea/algotrading-analysis-service/StudyZone/results/2022-06-19T135516-S001-01-ORB-OpeningRangeBreakout-6 month.csv"
    )

    # print(df.head())
    report_table = {
        "strategy": "",
        "data err": "",
        "data err %": "",
        "bullish": 0,
        "bearish": 0,
        "failed bullish": 0,
        "failed bearish": 0,
        "na": 0,
        "winning": 0,
        "winning %": 0,
        "losing": 0,
        "losing %": 0,
        "avg. win": 0,
        "avg. win %": 0,
        "avg. loss": 0,
        "avg. loss %": 0,
        "avg. time": 0,
        "avg. time %": 0,
        "avg. time (max)": 0,
        "avg. time (min)": 0,
        "drawdown (max)": 0,
        "drawdown (max) %": 0,
        "drawdown (min)": 0,
        "drawdown (min) %": 0,
        "drawdown (avg)": 0,
        "drawdown (avg) %": 0,
    }

    print(report_table)

    val = df["dir"].value_counts()
    for k, v in val.items():
        report_table[k.lower()] = v

    print(report_table)


generate_stock_report()
