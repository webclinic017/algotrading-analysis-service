from ast import IsNot
import os
from unittest import result
import pandas as pd
import json
import random
import matplotlib

matplotlib.use('Agg')
import matplotlib.style as mplstyle

mplstyle.use('fast')
import matplotlib.pyplot as plt
import finplot as fplt
from fpdf import FPDF
import mplfinance as mpf
from pandas import Timestamp

from datetime import datetime
from tqdm import tqdm

import App.DB.tsDB as db


def btResultsParser(env, dbConn, scan_dates, result, plot_images,
                    analysis_algorithm, analysis_symbol,
                    analysis_duration_backward):

    myDpi = 200
    charts_list = []

    file_id = str(random.randint(0, 999999))
    ftitle = datetime.now().strftime(
        "%Y-%m-%dT%H%M%S"
    ) + "-" + analysis_symbol + "-" + analysis_duration_backward

    generate_performance_report(result)

    f = os.getcwd() + "/StudyZone/results/" + file_id + "-" + ftitle
    f = f.replace(' ', '')
    result.to_csv(f + ".csv", index=False)

    # -------------------------------------------------------------------- Generate pdf (with charts)

    pdf = FPDF()
    pdf = FPDF(orientation='L', unit='mm', format='A4')

    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    author = "https://parag-b.github.io/algotrading-exchange-manager/"
    pdf.set_author(author)
    pdf.set_fill_color(153, 204, 255)
    pdf.set_title(file_id + "-" + ftitle)

    pdf.cell(0, 10, analysis_symbol, ln=1, align='C')
    pdf.cell(0, 10, analysis_algorithm, ln=1, align='C', fill=True)
    pdf.cell(0,
             10,
             datetime.now().strftime("%Y-%m-%d %-I:%M:%-S %p"),
             ln=1,
             align='C')

    pdf.set_margin(0)

    if plot_images is True:  # ------------------------------------- Draw charts

        print("Generating images #file-prefix-id: ", file_id)
        for dt in tqdm(scan_dates, colour='#4FD4B6'):

            image_title = analysis_symbol + " " + dt
            cdl = db.getCdlBtwnTime(env, dbConn, analysis_symbol, dt,
                                    ["09:00", "16:00"], "1")
            df_select = result[result["date"].astype(str).str[:10] == dt]

            hlines_level = []
            hlines_color = []
            hlines_style = []

            # {
            # "variable": "orb_high",
            # "value": "33233.6",
            # "drawing": "line",
            # "draw_fill": "solid",
            # "draw_color": "green"
            # }

            try:
                # print(df_select.iloc[0]["debug"])
                dbg_var = json.loads(df_select.iloc[0]["debug"])
                for vars in dbg_var:
                    if vars['drawing'] == 'line':
                        hlines_level.append(float(vars['value']))
                        hlines_color.append(vars['draw_color'][0])
                        if vars['draw_fill'] == 'dotted':
                            hlines_style.append('--')
                        else:
                            hlines_style.append('-')
            except Exception as e:
                print(e)

            if len(cdl):
                chart_file_name = file_id + "-" + image_title + '.png'
                charts_list.append(chart_file_name)
                # ------------------------------------------------- Generate Images
                if env['charting_sw'] == "finplot":

                    # `````````````````````finplot`````````````````````
                    fplt.candlestick_ochl(cdl[['open', 'close', 'high',
                                               'low']])

                    def save():
                        # import io
                        # f = io.BytesIO()
                        # fplt.screenshot(f)
                        fplt.screenshot(open(chart_file_name, 'wb'))
                        fplt.close()

                    fplt.timer_callback(
                        save, 0.4,
                        single_shot=True)  # wait some until we're rendered
                    fplt.show()

                else:
                    # `````````````````````matplotblib`````````````````````

                    fig = mpf.figure(style='yahoo')
                    fig, axlist = mpf.plot(cdl,
                                           type='candle',
                                           hlines=dict(hlines=hlines_level,
                                                       colors=hlines_color,
                                                       linestyle=hlines_style,
                                                       linewidths=1),
                                           volume=True,
                                           show_nontrading=True,
                                           style='yahoo',
                                           savefig=dict(fname=chart_file_name,
                                                        dpi=myDpi,
                                                        bbox_inches='tight',
                                                        pad_inches=0),
                                           returnfig=True)

                    for vars in dbg_var:
                        i = 0
                        # ax = [10]
                        if vars['drawing'] == 'line':
                            # ax[i] = fig.add_axes([0.15, 0.18, 0.70, 0.70])
                            axlist[i].text(
                                Timestamp(dt + " 09:30"),
                                float(vars['value']),
                                str(vars['variable']) + " " +
                                str(vars['value']),
                                #    color='white',
                                alpha=0.5)
                            i = i + 1

                    # savefig = dict(fname=chart_file_name,
                    #                dpi=myDpi,
                    #                bbox_inches='tight',
                    #                pad_inches=0)
                    fig.set_size_inches(18., 11.)
                    fig.savefig(chart_file_name, dpi=myDpi)

        # -------------------------------------------------------------------- Append charts to PDF Report

        print("Generating PDF with charts #file-prefix-id: ", file_id)
        for image_name in tqdm(charts_list, colour='#13B6D0'):
            pdf.image(image_name,
                      x=None,
                      y=None,
                      h=pdf.eph,
                      w=pdf.epw,
                      type='',
                      link='')
            os.remove(image_name)
            pdf.add_page()

    pdf.output(f + '.pdf', "F")  # ---------------------------------- Save PDF
    pdf.close()


def generate_performance_report(df):

    # print(df.head())
    result = df[df["status"].str.contains("signal-processed") == True]

    total_rows = len(df.index)
    err = df["status"].str.contains(r'ERR').sum()
    na = df["dir"].str.fullmatch(r'NA').sum(),
    bullish = df["dir"].str.fullmatch(r'Bullish').sum(),
    bearish = df["dir"].str.fullmatch(r'Bearish').sum(),
    failed_bullish = df["dir"].str.fullmatch(r'Failed Bullish').sum(),
    failed_bearish = df["dir"].str.fullmatch(r'Failed Bearish').sum(),

    report_summary = {
        "strategy": result.iloc[0]["strategy"],
        "instrument": result.iloc[0]["instr"],
        "total_data": total_rows,
        "data_err %": round((err / total_rows) * 100, 2),
        "bullish": bullish[0],
        "bearish": bearish[0],
        "failed_bullish": failed_bullish[0],
        "failed_bearish": failed_bearish[0],
        "na": na[0],
        "winning": 0,
        "winning %": 0,
        "losing": 0,
        "losing %": 0,
        "avg_win": 0,
        "avg_win %": 0,
        "avg_loss": 0,
        "avg_loss %": 0,
        "avg_time": 0,
        "avg_time_%": 0,
        "avg_time_(max)": 0,
        "avg_time_(min)": 0,
        "drawdown_(max)": 0,
        "drawdown_%_(max)": 0,
        "drawdown_(min)": 0,
        "drawdown_%_(min)": 0,
        "drawdown_(avg)": 0,
        "drawdown_%_(avg)": 0,
    }

    # json_object = json.dumps(report_summary, indent=4)

    # print(json_object)


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