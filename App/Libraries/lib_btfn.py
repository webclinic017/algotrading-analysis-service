def dbg(l, x, y, s, d):

    z = d.split("|")

    l.append(
        {
            "comment": s + " \n" + str(y),
            "value-x": str(x),
            "value-y": str(y),
            "drawing": z[0],
            "draw_fill": z[1],
            "draw_color": z[2],
        }
    )
    return l


def dbg_enter(l, df):
    if df.at[0, "dir"] != "NA":
        l.append(
            {
                "comment": str(df.at[0, "entry"])
                + "\n"
                + str(df.at[0, "entry_time"].time())
                + "\n"
                + "⚡ entry",
                "value-x": str(df.at[0, "entry_time"].time()),
                "value-y": str(df.at[0, "entry"]),
                "drawing": "vline",
                "draw_fill": "solid",
                "draw_color": "darkblue",
            }
        )
    return l


def dbg_exit(l, df):
    if df.at[0, "exit_reason"] != "":
        l.append(
            {
                "comment": str(df.at[0, "exit"])
                + "\n"
                + str(df.at[0, "exit_time"].time())
                + "\n"
                + "⚫ exit-"
                + str(df.at[0, "exit_reason"]),
                "value-x": str(df.at[0, "exit_time"].time()),
                "value-y": str(df.at[0, "exit"]),
                "drawing": "vline",
                "draw_fill": "solid",
                "draw_color": "purple",
            }
        )
    return l
