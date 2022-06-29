import os
import pandas as pd
import json
import random

from tqdm import tqdm
from datetime import datetime

import App.DB.tsDB as db
import App.Libraries.lib_pdf_generator as pdfg
import App.Libraries.lib_chart_generator_finplot as fpcg
import App.Libraries.lib_chart_generator_matplotlib as mplcg
import App.Libraries.lib_performance_report as pr


def btResultsParser(env, dbConn, result, plot_images, analysis_algorithm,
                    analysis_symbol, analysis_duration_backward):

    f, file_id, ftitle = derive_names(analysis_symbol,
                                      analysis_duration_backward)

    result, dates = get_dir_sorted_dates(result)

    report = pr.generate_performance_report("", result, "test1")

    # -------------------------------------------------------------------- Generate pdf (with charts)
    charts_list = []
    if plot_images is True:  # ------------------------------------- Draw charts
        print("Generating images #file-prefix-id: ", file_id)
        for dt in tqdm(dates, colour='#4FD4B6'):

            cdl = db.getCdlBtwnTime(env, dbConn, analysis_symbol, dt,
                                    ["09:00", "16:00"], "1")
            if len(cdl):
                df_select = result[result["date"].astype(str).str[:10] == dt]
                try:
                    dbg_var = json.loads(df_select.iloc[0]["debug"])
                except:
                    dbg_var = ""

                image_title = analysis_symbol + " " + dt
                chart_file_name = file_id + "-" + image_title + '.png'

                charts_list.append(chart_file_name + "^" + image_title +
                                   chart_header_infomartion(df_select))

                # ---------------------------------------------------------- Generate Images
                if env['charting_sw'] == "finplot":  # `````````````````````finplot
                    fpcg.generate_chart(cdl, chart_file_name)

                else:  # `````````````````````matplotblib
                    myDpi = 200
                    mplcg.generate_chart(dt, cdl, chart_file_name, myDpi,
                                         dbg_var)

        # -------------------------------------------------------------------- Append charts to PDF Report

    pdfg.generate_pdf_report(file_id + "-" + ftitle, analysis_symbol,
                             analysis_algorithm, f, charts_list, plot_images,
                             report)


def get_dir_sorted_dates(result):
    result = result.sort_values(by=['dir'])

    df = pd.DataFrame()
    df['date'] = pd.to_datetime(result['date'])

    dates = df['date'].dt.date

    return result, dates.astype(str).tolist()


# Builds string with split on '^', used by pdf generator for filename, imagename and text to be printed on chart page
def chart_header_infomartion(df_select):
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

    return "^" + df_select.iloc[0]["dir"] + "^" + str(res)

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


def derive_names(analysis_symbol, analysis_duration_backward):
    file_id = str(random.randint(0, 999999))
    ftitle = datetime.now().strftime(
        "%Y-%m-%d__%-I:%M%p"
    ) + "-" + analysis_symbol + "-" + analysis_duration_backward
    f = os.getcwd() + "/StudyZone/results/" + file_id + "-" + ftitle
    f = f.replace(' ', '')

    return f, file_id, ftitle
