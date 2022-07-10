import matplotlib
import mplfinance as mpf

matplotlib.use("Agg")
import matplotlib.style as mplstyle

mplstyle.use("fast")
import matplotlib.pyplot as plt
from pandas import Timestamp


def generate_chart(dt, cdl, chart_file_name, myDpi, dbg_var):

    hlines, vlines = calculate_hvlines_info(dt, dbg_var)
    fig = mpf.figure(style="yahoo")
    fig, axlist = mpf.plot(
        cdl,
        type="candle",
        #    title=image_title,
        hlines=hlines,
        vlines=vlines,
        volume=True,
        show_nontrading=True,
        style="yahoo",
        savefig=dict(
            fname=chart_file_name, dpi=myDpi, bbox_inches="tight", pad_inches=0
        ),
        returnfig=True,
    )

    axlist = calculate_text_markers(axlist, dt, dbg_var)

    fig.set_size_inches(18.0, 11.0)
    fig.savefig(chart_file_name, dpi=myDpi)
    plt.close("all")


def calculate_text_markers(axlist, dt, dbg_var):
    for vars in dbg_var:  # ---------- print markers/info on chart
        if len(vars):
            axlist[0].text(
                Timestamp(dt + " " + vars["value-x"]),
                float(vars["value-y"]),
                vars["comment"],
                alpha=0.5,
            )

    return axlist


def calculate_hvlines_info(dt, dbg_var):
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

    for vars in dbg_var:
        if len(vars):
            if vars["drawing"] == "hline":
                hlines_level.append(float(vars["value-y"]))
                hlines_color.append(vars["draw_color"])
                hlines_style.append(vars["draw_fill"])
            elif vars["drawing"] == "vline":
                vlines_level.append(dt + " " + (vars["value-x"]))
                vlines_color.append(vars["draw_color"])
                vlines_style.append(vars["draw_fill"])

    hlines = dict(
        hlines=hlines_level,
        colors=hlines_color,
        linestyle=hlines_style,
        linewidths=1,
        alpha=0.4,
    )

    vlines = dict(
        vlines=vlines_level,
        colors=vlines_color,
        linestyle=vlines_style,
        linewidths=1,
        alpha=0.4,
    )

    return hlines, vlines
