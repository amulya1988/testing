import os
import tempfile

import PyPDF2
from pdfrw import PdfWriter, PdfReader

from base_util import project_url, pdf_dir
from pdf import pdf_util
from pdf.pdf_util import pdf_watermark_page


def gen_report(report_json):
    print(report_json)

    template_pdf = report_json.get("template")

    pdf_list = []
    for report in report_json.get("pages"):
        if report.get("TYPE") == "HTML":
            pdf_list.extend(
                generate_stamped_page(pdf_util.pdf_from_url(report.get("URL")), template_pdf=template_pdf,
                                      stamp_page=report.get("STAMP_PAGE")))

        elif report.get("TYPE") == "PDF":
            pdfpage = PyPDF2.PdfFileReader(open(os.path.join(pdf_dir, template_pdf), "rb")).getPage(
                report.get("PAGE_NO"))
            pdf_list.append(pdfpage)
    return pdf_list


def generate_stamped_page(pdf_report, template_pdf, stamp_page=None):
    output_raw_path = tempfile.mktemp(suffix=".pdf")
    with open(output_raw_path, 'wb') as file:
        file.write(pdf_report)
    pages = pdf_watermark_page(output_raw_path, stamp_page, template_pdf)
    return pages


def generate_pdf_report(PROJ_ID):
    html_reports = ["{0}/individual-report/{1}/{2}".format(project_url, section, PROJ_ID) for section in
                    ["front_page"]]
    print(html_reports)
    return pdf_util.pdf_from_url(report_list=html_reports)


def merge_pdf(pdf_list):
    pdf_io = tempfile.mktemp(suffix=".pdf")

    writer = PdfWriter()
    for pdfFileObj in pdf_list:
        writer.addpages(PdfReader(fdata=pdfFileObj).pages)
    writer.write(pdf_io)
    return pdf_io


def merge_page_stamp(stamp_pdf_path, page):
    watermark = PyPDF2.PdfFileReader(stamp_pdf_path).getPage(0)
    page.mergePage(watermark)
    return page
