import os
import math
from fpdf import FPDF
from tqdm import tqdm
from datetime import datetime

import App.DB.tsDB as db


def generate_pdf_report(
    fname, analysis_symbol, analysis_algorithm, f, charts_list, plot_images, report_data
):
    print("Generating PDF : ", fname + ".pdf")
    # print(report_data)
    pdf = FPDF()
    pdf = FPDF(orientation="L", unit="mm", format="A4")

    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    author = "https://parag-b.github.io/algotrading-exchange-manager/"
    pdf.set_author(author)
    pdf.set_fill_color(153, 204, 255)
    pdf.set_title(fname)

    # ----------------------------------------------------------- insert file heading
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(0, 10, analysis_symbol, ln=1, align="C")
    pdf.cell(0, 10, analysis_algorithm, ln=1, align="C", fill=True)
    pdf.cell(0, 10, datetime.now().strftime("%Y-%m-%d %-I:%M:%-S %p"), ln=1, align="C")
    pdf.set_text_color(r=155, g=155, b=255)

    # ----------------------------------------------------------- insert Table-Of-Content
    pages = int(round_up(len(charts_list) / 30))  # count pages req for toc
    # 30 is no of rows in TOC printed based on current setting. Count actual no of lines per page in ToC
    # in some bounday case, it may fail. Need to define more tighter logic or precise list on toc/page

    if plot_images:
        pdf.insert_toc_placeholder(render_toc, pages=pages)
    pdf.set_text_color(r=0, g=0, b=0)

    # ----------------------------------------------------------- insert simulation summary report
    generate_report_table(pdf, report_data)

    # ----------------------------------------------------------- insert charts
    section = ""
    for info_string in tqdm(charts_list, colour="#13B6D0"):
        pdf.add_page()
        info_list = info_string.split("^")
        image_name = info_list.pop(0)
        header = info_list.pop(0)

        # ------------------------------------------ mark new section (bullish/bearish/na/...)
        if section != info_list[0]:
            pdf.start_section("Charts with " + info_list[0].capitalize(), level=1)
            section = info_list[0]
            subsection_num = 1

        # ------------------------------------------ mark new sub-section for individual charts
        pdf.start_section(
            "   ~ " + str(subsection_num) + " " + header.capitalize(), level=2
        )
        subsection_num += 1

        pdf.cell(0, 0, header, ln=1, align="C")
        pdf.set_font(family=None, style="", size=10)
        pdf.set_text_color(r=0, g=0, b=255)
        for val in info_list:  # --------------------- print information above chart
            pdf.write(h=10, txt=val + "\t", link="", print_sh=False)
        pdf.set_text_color(r=0, g=0, b=0)

        if plot_images:  # ---------------------------------- insert chart
            pdf.image(
                image_name, x=0, y=20, h=pdf.eph - 20, w=pdf.epw, type="", link=""
            )
            os.remove(image_name)

    pdf.output(f + ".pdf", "F")  # ---------------------------------- Save PDF
    pdf.close()


def generate_report_table(pdf, report):

    pdf.start_section("Simulation Report", level=1)

    pdf.set_font(size=10)
    pdf.ln(pdf.font_size * 2)

    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4  # distribute content evenly

    split = 0
    for row in report.items():
        if row[0].find("new-section") >= 0:
            if split == 1:  # odd no of cells, print a line to reserve space
                pdf.ln(8)
            # pdf.ln(1)
            pdf.set_fill_color(253, 242, 233)
            pdf.set_font(style="B")  # enabling bold text)
            pdf.cell(0, 8, row[1].upper(), border=1, ln=1, align="C", fill=True)
            pdf.set_font(style="")
            split = 0
        else:
            split += 1
            for datum in row:
                pdf.multi_cell(
                    col_width,
                    line_height,
                    datum.title().replace("_", " "),
                    border=1,
                    new_x="RIGHT",
                    new_y="TOP",
                    max_line_height=pdf.font_size,
                    fill=False,
                )
            if split == 2:
                pdf.ln(line_height)
                split = 0


def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier


def render_toc(pdf, outline):
    # pdf.y += 30
    pdf.set_font("Helvetica", size=16)
    pdf.underline = True
    pdf.multi_cell(
        w=pdf.epw,
        h=pdf.font_size,
        txt="Table of contents:",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.underline = False
    pdf.x += 10
    pdf.y += 10
    pdf.set_font(size=10)
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
            new_x="LEFT",
            new_y="NEXT",
            align="L",
            link=link,
        )
