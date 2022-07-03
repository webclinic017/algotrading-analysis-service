def generate_chart(cdl, chart_file_name):

    import finplot as fplt

    fplt.candlestick_ochl(cdl[["open", "close", "high", "low"]])

    def save():
        # import io
        # f = io.BytesIO()
        # fplt.screenshot(f)
        fplt.screenshot(open(chart_file_name, "wb"))
        fplt.close()

    fplt.timer_callback(save, 0.4, single_shot=True)  # wait some until we're rendered
    fplt.show()
