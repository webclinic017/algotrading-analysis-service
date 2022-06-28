import os
import pandas as pd
import json
import random
import matplotlib
import mplfinance as mpf
import App.DB.tsDB as db

from tqdm import tqdm
from pandas import Timestamp
from datetime import datetime

matplotlib.use('Agg')
import matplotlib.style as mplstyle

mplstyle.use('fast')
import matplotlib.pyplot as plt
import finplot as fplt

import App.Libraries.lib_pdf_generator as pdfg


def btResultsParser(env, dbConn, scan_dates, result, plot_images,
                    analysis_algorithm, analysis_symbol,
                    analysis_duration_backward):

    myDpi = 200
    charts_list = []

    file_id = str(random.randint(0, 999999))
    ftitle = datetime.now().strftime(
        "%Y-%m-%d__%-I:%M%p"
    ) + "-" + analysis_symbol + "-" + analysis_duration_backward

    generate_performance_report(result)

    f = os.getcwd() + "/StudyZone/results/" + file_id + "-" + ftitle
    f = f.replace(' ', '')
    result.to_csv(f + ".csv", index=False)

    # -------------------------------------------------------------------- Generate pdf (with charts)

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
            vlines_level = []
            vlines_color = []
            vlines_style = []

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
                    if vars['drawing'] == 'hline':
                        hlines_level.append(float(vars['value-y']))
                        hlines_color.append(vars['draw_color'])
                        if vars['draw_fill'] == 'dotted':
                            hlines_style.append('--')
                        else:
                            hlines_style.append('-')
                    elif vars['drawing'] == 'vline':
                        vlines_level.append(dt + " " + (vars['value-x']))
                        vlines_color.append(vars['draw_color'])
                        if vars['draw_fill'] == 'dotted':
                            vlines_style.append('--')
                        else:
                            vlines_style.append('-')

                            # vlines=dict(vlines='2019-11-18',linewidths=125,alpha=0.4)
            except:
                dbg_var = ""

            if len(cdl):
                chart_file_name = file_id + "-" + image_title + '.png'

                if df_select.iloc[0]["dir"] == 'bullish':
                    res = df_select.iloc[0]["exit"] - df_select.iloc[0]["entry"]
                elif df_select.iloc[0]["dir"] == 'bearish':
                    res = df_select.iloc[0]["entry"] - df_select.iloc[0]["exit"]
                else:
                    res = 0

                if res < 0:
                    res = 'Loss - ' + str(res)
                elif res > 0:
                    res = 'Profit - ' + str(res)
                else:
                    res = ""

                charts_list.append(chart_file_name + "^" + image_title + "^" +
                                   df_select.iloc[0]["dir"] + "^" + str(res))

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
                    fig, axlist = mpf.plot(
                        cdl,
                        type='candle',
                        #    title=image_title,
                        hlines=dict(hlines=hlines_level,
                                    colors=hlines_color,
                                    linestyle=hlines_style,
                                    linewidths=1,
                                    alpha=0.4),
                        vlines=dict(vlines=vlines_level,
                                    colors=vlines_color,
                                    linestyle=vlines_style,
                                    linewidths=1,
                                    alpha=0.4),
                        volume=True,
                        show_nontrading=True,
                        style='yahoo',
                        savefig=dict(fname=chart_file_name,
                                     dpi=myDpi,
                                     bbox_inches='tight',
                                     pad_inches=0),
                        returnfig=True)

                    for vars in dbg_var:  # ---------- print markers/info on chart
                        axlist[0].text(Timestamp(dt + " " + vars['value-x']),
                                       float(vars['value-y']),
                                       str(vars['variable']) + " " +
                                       str(vars['value-print']),
                                       alpha=0.5)

                    fig.set_size_inches(18., 11.)
                    fig.savefig(chart_file_name, dpi=myDpi)

        # -------------------------------------------------------------------- Append charts to PDF Report

    pdfg.generate_pdf_report(file_id + "-" + ftitle, analysis_symbol,
                             analysis_algorithm, f, charts_list, plot_images)


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


def render_toc(pdf, outline):
    pdf.y += 50
    pdf.set_font("Helvetica", size=16)
    pdf.underline = True
    p(pdf, "Table of contents:")
    pdf.underline = False
    pdf.y += 20
    pdf.set_font("Courier", size=12)
    for section in outline:
        link = pdf.add_link()
        pdf.set_link(link, page=section.page_number)
        text = f'{" " * section.level * 2} {section.name}'
        text += (
            f' {"." * (60 - section.level*2 - len(section.name))} {section.page_number}'
        )
        pdf.multi_cell(
            w=pdf.epw,
            h=pdf.font_size,
            txt=text,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
            link=link,
        )


def p(pdf, text, **kwargs):
    pdf.multi_cell(
        w=pdf.epw,
        h=pdf.font_size,
        txt=text,
        new_x="LMARGIN",
        new_y="NEXT",
        **kwargs,
    )