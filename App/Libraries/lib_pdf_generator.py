import os
import math
from tqdm import tqdm
from fpdf import FPDF
from datetime import datetime

import App.DB.tsDB as db


def generate_pdf_report(fname, analysis_symbol, analysis_algorithm, f,
                        charts_list, plot_images):

    print("Generating PDF : ", fname + '.pdf')
    pdf = FPDF()
    pdf = FPDF(orientation='L', unit='mm', format='A4')

    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    author = "https://parag-b.github.io/algotrading-exchange-manager/"
    pdf.set_author(author)
    pdf.set_fill_color(153, 204, 255)
    pdf.set_title(fname)

    pdf.set_text_color(r=0, g=0, b=0)
    pdf.cell(0, 10, analysis_symbol, ln=1, align='C')
    pdf.cell(0, 10, analysis_algorithm, ln=1, align='C', fill=True)
    pdf.cell(0,
             10,
             datetime.now().strftime("%Y-%m-%d %-I:%M:%-S %p"),
             ln=1,
             align='C')

    pdf.add_page()
    pages = int(round_up(len(charts_list) / 30))
    # 30 is no of rows in TOC printed based on current setting. Count actual no of lines per page in ToC

    pdf.set_text_color(r=155, g=155, b=255)
    if plot_images:
        pdf.insert_toc_placeholder(render_toc, pages=pages)
    pdf.set_text_color(r=0, g=0, b=0)

    section = ""
    section_num = 0
    for info_string in tqdm(charts_list, colour='#13B6D0'):
        pdf.add_page()
        info_list = info_string.split("^")
        image_name = info_list.pop(0)
        header = info_list.pop(0)

        # new section
        if section != info_list[0]:
            section_num += 1
            pdf.start_section(str(section_num) + " " + info_list[0], level=1)
            section = info_list[0]
            subsection_num = 1

        pdf.start_section("    " + str(section_num) + "." +
                          str(subsection_num) + " " + header,
                          level=1)
        subsection_num += 1

        pdf.cell(0, 0, header, ln=1, align='C')

        pdf.set_font(family=None, style='', size=10)

        pdf.set_text_color(r=0, g=0, b=255)
        for val in info_list:
            pdf.write(h=10, txt=val + "\t", link='', print_sh=False)
        pdf.set_text_color(r=0, g=0, b=0)

        if plot_images:
            pdf.image(image_name,
                      x=0,
                      y=20,
                      h=pdf.eph - 20,
                      w=pdf.epw,
                      type='',
                      link='')
            os.remove(image_name)

    pdf.output(f + '.pdf', "F")  # ---------------------------------- Save PDF
    pdf.close()


def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier


def render_toc(pdf, outline):
    # pdf.y += 30
    pdf.set_font("Helvetica", size=16)
    pdf.underline = True
    p(pdf, "Table of contents:")
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


def p(pdf, text, **kwargs):
    pdf.multi_cell(
        w=pdf.epw,
        h=pdf.font_size,
        txt=text,
        new_x="LMARGIN",
        new_y="NEXT",
        **kwargs,
    )
