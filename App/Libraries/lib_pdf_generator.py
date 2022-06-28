import os
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

    pdf.cell(0, 10, analysis_symbol, ln=1, align='C')
    pdf.cell(0, 10, analysis_algorithm, ln=1, align='C', fill=True)
    pdf.cell(0,
             10,
             datetime.now().strftime("%Y-%m-%d %-I:%M:%-S %p"),
             ln=1,
             align='C')

    # pdf.set_margin(0)
    pdf.insert_toc_placeholder(render_toc)

    for info_string in tqdm(charts_list, colour='#13B6D0'):
        pdf.add_page()
        info_list = info_string.split("^")
        image_name = info_list.pop(0)
        header = info_list.pop(0)
        pdf.start_section(header, level=1)
        pdf.cell(0, 0, header, ln=1, align='C')

        pdf.set_font(family=None, style='', size=10)

        for val in info_list:
            pdf.write(h=10, txt=val + "\t", link='', print_sh=False)

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
