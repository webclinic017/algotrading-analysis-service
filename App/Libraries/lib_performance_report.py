import pandas as pd


def generate_performance_report(fin, df, fout):

    # print(df.head())
    if fin != "":
        df = pd.read_csv(fin)

    result = df[df["status"].str.contains("signal-processed") == True]

    total_rows = len(df.index)
    err = df["status"].str.contains(r'ERR').sum()
    na = df["dir"].str.fullmatch(r'NA').sum(),
    bullish = df["dir"].str.fullmatch(r'Bullish').sum(),
    bearish = df["dir"].str.fullmatch(r'Bearish').sum(),
    failed_bullish = df["dir"].str.fullmatch(r'Failed Bullish').sum(),
    failed_bearish = df["dir"].str.fullmatch(r'Failed Bearish').sum(),

    report_summary_basic = {
        "strategy": result.iloc[0]["strategy"],
        "instrument": result.iloc[0]["instr"],
    }
    report_summary_data = {
        "total_data": str(total_rows),
        "data_err %": str(round((err / total_rows) * 100, 2)),
    }
    report_summary_statistics = {
        "bullish": str(bullish[0]),
        "bearish": str(bearish[0]),
        "failed_bullish": str(failed_bullish[0]),
        "failed_bearish": str(failed_bearish[0]),
        "na": str(na[0]),
        "none": "none",
    }
    report_summary_winlose = {
        "winning": str(0),
        "winning_%": str(0),
        "losing": str(0),
        "losing_%": str(0),
    }
    report_summary_avg = {
        "avg_win": str(0),
        "avg_win_%": str(0),
        "avg_loss": str(0),
        "avg_loss_%": str(0),
        "avg_time": str(0),
        "avg_time_%": str(0),
        "avg_time_(max)": str(0),
        "avg_time_(min)": str(0),
    }
    report_summary_drawdown = {
        "drawdown_(max)": str(0),
        "drawdown_%_(max)": str(0),
        "drawdown_(min)": str(0),
        "drawdown_%_(min)": str(0),
        "drawdown_(avg)": str(0),
        "drawdown_%_(avg)": str(0),
    }

    report_summary = []
    report_summary.append(report_summary_basic)
    report_summary.append(report_summary_data)
    report_summary.append(report_summary_statistics)
    report_summary.append(report_summary_winlose)
    report_summary.append(report_summary_avg)
    report_summary.append(report_summary_drawdown)

    print("Generating PDF : ", fout + '.pdf')
    from fpdf import FPDF

    pdf = FPDF()
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_display_mode(zoom="fullwidth", layout="continuous")
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.set_fill_color(153, 204, 255)
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(0,
             10,
             'Performance Report of ' + result.iloc[0]["strategy"] + " on " +
             result.iloc[0]["instr"],
             ln=1,
             align='C',
             fill=True)

    pdf.set_font(size=10)

    pdf.ln(pdf.font_size * 2)

    print_table(pdf, "Win/lose Ration", report_summary_winlose)
    print_table(pdf, "Averages", report_summary_avg)
    print_table(pdf, "Drawdown", report_summary_drawdown)
    pdf.ln(pdf.font_size * 2)
    print_table(pdf, "Stats", report_summary_statistics)
    print_table(pdf, "Data", report_summary_data)

    pdf.output(fout + '.pdf')

    # print(report_summary)

    # df.to_csv(fout + ".csv", index=False)


def print_table(pdf, header, dlist):

    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4  # distribute content evenly

    # pdf.ln(pdf.font_size * 1)

    # pdf.set_fill_color(153, 204, 255)
    pdf.set_fill_color(253, 242, 233)
    pdf.set_font(style="B")  # enabling bold text)
    pdf.cell(0, 8, header, border=1, ln=1, align='C', fill=True)
    pdf.set_font(style="")

    split = 0
    fill = 0
    for row in dlist.items():
        split += 1
        for datum in row:
            pdf.multi_cell(col_width,
                           line_height,
                           datum.title().replace("_", " "),
                           border=1,
                           new_x="RIGHT",
                           new_y="TOP",
                           max_line_height=pdf.font_size,
                           fill=False)
        if split == 2:
            pdf.ln(line_height)
            fill = not fill
            split = 0