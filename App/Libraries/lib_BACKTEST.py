import os
import pandas as pd

import random
import matplotlib

matplotlib.use('Agg')
import mplfinance as mpf

from datetime import datetime
from tqdm import tqdm

import App.DB.tsDB as db


def btResultsParser(env, dbConn, scan_dates, result, plot_images,
                    analysis_algorithm, analysis_symbol,
                    analysis_duration_backward):

    file_id = random.randint(0, 999999)
    file_id = str(file_id)

    # generate_stock_report

    # round digits
    # data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']] = \
    # data[['Entry', 'Target', 'SL', 'Exit', 'Result', 'ResultPerc', 'SMax', 'SMin', 'SMaxD', 'SMinD']].astype(float).round(1)

    # print('Results: ', data['Result'].sum().astype(float).round(1))
    # print(result["dir"].value_counts())
    # print(data['Signal'].value_counts())
    # print(data["time"].dt.strftime("%Y-%m-%d %H:%M:%S"))

    # store to csv file
    ftitle = datetime.now().strftime(
        "%Y-%m-%dT%H%M%S"
    ) + "-" + analysis_symbol + "-" + analysis_duration_backward

    f = os.getcwd() + "/StudyZone/results/" + file_id + "-" + ftitle
    f = f.replace(' ', '')
    result.to_csv(f + ".csv", index=False)

    # -------------------------------------------------------------------- generate pdf (with charts)
    from fpdf import FPDF
    fpdf = FPDF(orientation='L', unit='mm', format='A4')

    fpdf.add_page()
    fpdf.set_font("Arial", "B", 16)
    author = "https://parag-b.github.io/algotrading-exchange-manager/"
    fpdf.set_author(author)
    fpdf.set_fill_color(153, 204, 255)
    fpdf.set_title(ftitle)

    fpdf.cell(0, 10, analysis_symbol, ln=1, align='C')
    fpdf.cell(0, 10, analysis_algorithm, ln=1, align='C', fill=True)
    fpdf.cell(0,
              10,
              datetime.now().strftime("%Y-%m-%d %-I:%M:%-S %p"),
              ln=1,
              align='C')

    myDpi = 250
    file_id = random.randint(0, 999999)
    file_id = str(file_id)

    charts_list = []

    if plot_images is True:
        from fpdf import FPDF

        print("Generating images #file-prefix-id: ", file_id)
        for dt in tqdm(scan_dates, colour='#4FD4B6'):

            image_title = analysis_symbol + " " + dt
            cdl = db.getCdlBtwnTime(env, dbConn, analysis_symbol, dt,
                                    ["09:00", "16:00"], "1")

            if len(cdl):
                # print("Generating image: ", image_title + '.png')
                chart_file_name = file_id + "-" + image_title + '.png'
                charts_list.append(chart_file_name)

                mpf.plot(
                    cdl,
                    type='candle',
                    title=dict(title=image_title, y=1.05, fontsize=10, x=0.59),
                    volume=True,
                    show_nontrading=True,
                    style='yahoo',
                    #  figsize=(5, 6),
                    savefig=dict(fname=chart_file_name,
                                 dpi=myDpi,
                                 bbox_inches='tight',
                                 pad_inches=0))

        print("Generating PDF with charts #file-prefix-id: ", file_id)
        for image_name in tqdm(charts_list, colour='#13B6D0'):
            # for image_name in charts_list:

            fpdf.image(
                image_name,
                x=None,
                y=None,
                w=myDpi - 50,
                #    h=500,
                type='',
                link='')

            os.remove(image_name)
            # print("Deleting file: ", image_name)

            fpdf.add_page()

    fpdf.output(f + '.pdf', "F")
    fpdf.close()


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


# generate_stock_report()

# def recordExtremes(dayDF, selectedDate, strategy):

#     max_index = dayDF["Close"].idxmax()
#     min_index = dayDF["Close"].idxmin()

#     strategy.at[0, 'SMax'] = dayDF.at[max_index, 'Close']
#     strategy.at[0, 'SMaxTime'] = pd.to_datetime(max_index).time().strftime(
#         "%H:%M")
#     strategy.at[0, 'SMaxD'] = strategy.at[0, 'SMax'] - strategy.at[0, 'Entry']

#     strategy.at[0, 'SMin'] = dayDF.at[min_index, 'Close']
#     strategy.at[0, 'SMinTime'] = pd.to_datetime(min_index).time().strftime(
#         "%H:%M")
#     strategy.at[0, 'SMinD'] = strategy.at[0, 'Entry'] - strategy.at[0, 'SMin']

#     return