import json
import tempfile

import PyPDF2
from flask import Blueprint, make_response

from base_util import project_url
from database.db_config import close_session, create_session
from pdf.pdf_gen import gen_report, merge_page_stamp
from pdf.pdf_util import get_stamp_pdf
from repository.crud_repository import UserRepository

pdf_app = Blueprint('pdf', __name__)


@pdf_app.route('/<int:bpm_id>', methods=['GET'])
def pdf_report(bpm_id):
    session_con, con = create_session()
    project = UserRepository(session_con).find_bpm_id(bpm_id)

    report_template = json.loads(project.group.reporttemplate.TEMPLATE_JSON)

    def prepare_report_json(data):
        if data.get("TYPE") == "HTML":
            data["URL"] = data.get("URL").format(project_url=project_url, bpm_id=bpm_id)
        return data

    report_json = {"template": report_template.get("template"),
                   "pages": [prepare_report_json(x) for x in report_template.get("pages")]}

    pages = gen_report(report_json)

    output = PyPDF2.PdfFileWriter()
    for page_no in range(len(pages)):
        page = pages[page_no]
        if page_no > 0:
            stamp_pdf_path = get_stamp_pdf(project.PROJ_NAME, page_no)
            merge_page_stamp(stamp_pdf_path, page)
        output.addPage(page)

    output_path = tempfile.mktemp(suffix=".pdf")
    outputStream = open(output_path, "wb")
    output.write(outputStream)
    outputStream.close()

    close_session(session_con, con)
    response = make_response(open(output_path, "rb").read())
    response.headers['Content-Disposition'] = 'attachment; filename=Feedback Report.pdf'
    response.headers["Content-type"] = "application/pdf"
    return response
