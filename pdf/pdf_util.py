import os
import tempfile

import PyPDF2
import pdfkit
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from base_util import pdf_config, basepath, font_dir, config

report_path = os.path.join(os.path.join(basepath, "static"), "report")
pdfmetrics.registerFont(TTFont('Segoe UI', os.path.join(font_dir, "Cambria.ttf")))


def pdf_from_url_wkhtltopdf(report_list, page_size="A4", orientation="Portrait"):
    options = {
        'page-size': page_size,
        'orientation': orientation,
        'dpi': 72,
        'encoding': "UTF-8"
    }

    return pdfkit.from_url(report_list, output_path=False, configuration=pdf_config,
                           options=options)


def pdf_from_url_pychrometopdf(report_list, page_size="A4", orientation="Portrait"):
    pdf_path = tempfile.mktemp(suffix=".pdf")
    print(pdf_path)
    os.system(
        """chrome-headless-render-pdf --paper-width 8.27 --paper-height 11.69 --chrome-binary {chrome_binary} --chrome-option=--no-sandbox --url {report_url} --pdf {pdf_path}""".format(
            chrome_binary=config.get("PDF", 'chrome_binary'), report_url=report_list, pdf_path=pdf_path))
    with open(pdf_path, "rb") as pdf_file:
        return pdf_file.read()


def pdf_from_url(report_list, page_size="A4", orientation="Portrait"):
    return pdf_from_url_pychrometopdf(report_list, page_size, orientation)


def pdf_watermark(file_read_path, PROJ_NAME, page_no, stamping=False):
    pdf_in = PyPDF2.PdfFileReader(file_read_path)

    watermark = PyPDF2.PdfFileReader(os.path.join(report_path, "long.pdf")).getPage(page_no)

    output = PyPDF2.PdfFileWriter()

    for i in range(pdf_in.getNumPages()):
        page = pdf_in.getPage(i)
        page.mergePage(watermark)

        output.addPage(page)

    output_path = tempfile.mktemp(suffix=".pdf")
    outputStream = open(output_path, "wb")
    output.write(outputStream)
    outputStream.close()

    # out = BytesIO()
    # output.write(stream=out)
    return output_path


def pdf_watermark_page(pdf_report, page_no, template_pdf):
    pdf_in = PyPDF2.PdfFileReader(pdf_report)
    # pdf_in = PyPDF2.PdfFileReader(file_read_path)

    watermark = PyPDF2.PdfFileReader(os.path.join(report_path, template_pdf)).getPage(page_no)

    output = []

    for i in range(pdf_in.getNumPages()):
        page = pdf_in.getPage(i)
        page.mergePage(watermark)

        output.append(page)

    return output


def get_stamp_pdf(PROJ_NAME, PAGE_NO):
    from reportlab.pdfgen import canvas
    out_path = tempfile.mktemp(suffix=".pdf")
    canvas = canvas.Canvas(out_path, pagesize=A4)
    canvas.setLineWidth(.3)
    canvas.setFont('Segoe UI', 8)
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setFillColorRGB(0, 0, 0)
    canvas.drawString(30, 10, "Feedback Report for {0}".format(PROJ_NAME))
    canvas.drawString(540, 10, "Page {0}".format(PAGE_NO))
    canvas.save()
    return out_path


if __name__ == '__main__':
    pdf_from_url_pychrometopdf(["http://localhost:9992/long-report/front_page/74"])
