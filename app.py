from flask import Flask, render_template, request, jsonify, current_app, session
from fillpdf import fillpdfs
from pdfrw import PdfReader as PdfRwReader, PdfWriter as PdfRwWriter, PageMerge, PdfDict, PdfName
from datetime import datetime, date, timedelta
import os
import json

from pdf_fillers import fill_cf1, fill_cf2, fill_csf, fill_soa
from pdf_utils import clean_files

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "ABTC"
# PdfWriter().write(output_pdf, pdf)

# Send the filled PDF as a download
# send_file(output_pdf, as_attachment=True)
# Access form fields
# if reader.get_fields():
#     print("PDF has fillable form fields!")
#     fields = reader.get_fields()
#     for field_name, field_info in fields.items():
#         print(f"Field name: {field_name}, type: {field_info.get('/FT')}")
# else:
#     print("PDF does NOT have fillable form fields.")

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/submit_form", methods=["POST"])
def submit_form():
    data = request.get_json()
    pretty_json_string = json.dumps(data, indent=4)
    patient_data = dict(data)
    session['patient_data'] = patient_data
    print(pretty_json_string)
    clean_files(["output_cf1.pdf", "output_cf2.pdf", "output_csf.pdf", "output_soa.pdf"], current_app.root_path)

    fill_cf1(patient_data)
    fill_csf(patient_data)
    fill_cf2(patient_data)
    fill_soa(patient_data)

    return jsonify({"status": "success", "message": "Form received"})


@app.route("/view_print")
def view_print_pdf():
    pdf_files = [
        {"name": "CF-1 Form", "url": "/static/pdfs/output_cf1.pdf"},
        {"name": "CF-2 Form", "url": "/static/pdfs/output_cf2.pdf"},
        {"name": "CSF Form", "url": "/static/pdfs/output_csf.pdf"},
    ]
    statement = load_json(os.path.join(os.path.dirname(__file__), 'json', 'statement-data.json'))
    patient = session.get('patient_data', {})

    patientName = " ".join(filter(None, [
        patient.get('firstName'),
        patient.get('middleName'),
        patient.get('lastName'),
        patient.get('nameExt')
    ]))
    statement["patientInfo"]['left'][0]['value'] = patientName
    
    fee_summary = load_json(os.path.join(os.path.dirname(__file__), 'json', 'fee-summary.json'))
    professional_fees = load_json(os.path.join(os.path.dirname(__file__), 'json', 'professional-fees.json'))
    itemized_charges = load_json(os.path.join(os.path.dirname(__file__), 'json', 'itemized-charges.json'))
    return render_template('viewPrintPDF.html', pdf_files=pdf_files,  header=statement['header'],
                         patient_info=statement['patientInfo'],
                         fee_summary=fee_summary,
                         professional_fees=professional_fees,
                         itemized_charges=itemized_charges)


def load_json(filename):
    with open(filename, 'r') as f:
        print()
        return json.load(f)

@app.route("/reports")
def view_reports():
    return render_template('reports.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
