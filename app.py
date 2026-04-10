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
    clean_files(["output_cf1.pdf", "output_cf2.pdf",
                "output_csf.pdf", "output_soa.pdf"], current_app.root_path)

    fill_cf1(patient_data)
    fill_csf(patient_data)
    fill_cf2(patient_data)
    # fill_soa(patient_data)

    return jsonify({"status": "success", "message": "Form received"})


@app.route("/view_print")
def view_print_pdf():
    pdf_files = [
        {"name": "CF-1 Form", "url": "/static/pdfs/output_cf1.pdf"},
        {"name": "CF-2 Form", "url": "/static/pdfs/output_cf2.pdf"},
        {"name": "CSF Form", "url": "/static/pdfs/output_csf.pdf"},
    ]
    statement = load_json(os.path.join(os.path.dirname(
        __file__), 'json', 'statement-data.json'))
    patient = session.get('patient_data', {})

    patientDOB = ""

    if patient.get('dependent'):
        dependent = patient.get('dependent', {})
        patientName = " ".join(filter(None, [
            dependent.get('depFname'),
            dependent.get('depMname'),
            dependent.get('depLname'),
            dependent.get('depExt')
        ]))
        patientDOB = calculate_age_month_days(
        dependent.get('depDob'))

    else:
        patientName = " ".join(filter(None, [
            patient.get('firstName'),
            patient.get('middleName'),
            patient.get('lastName'),
            patient.get('nameExt')
        ]))
        patientDOB = calculate_age_month_days(
        patient.get('dob'))

    patientAddress = " ".join(filter(None, [
        patient.get('barangay'),
        patient.get('municipality') + ", Leyte",
    ]))


    statement["patientInfo"]['left'][0]['value'] = patientName
    statement["patientInfo"]['left'][1]['value'] = patientAddress
    statement["patientInfo"]['right'][0]['value'] = patientDOB
    statement["patientInfo"]['right'][1]['value'] = format_datetime(
        patient.get('datetimeAdmitted', ''))
    statement["patientInfo"]['right'][2]['value'] = format_datetime(
        patient.get('datetimeDischarged', ''))

    fee_summary = load_json(os.path.join(
        os.path.dirname(__file__), 'json', 'fee-summary.json'))
    professional_fees = load_json(os.path.join(
        os.path.dirname(__file__), 'json', 'professional-fees.json'))
    itemized_charges = load_json(os.path.join(
        os.path.dirname(__file__), 'json', 'itemized-charges.json'))

    patient_age = calculate_age(patient.get('dob', ''))

    if patient_age >= 60:
        fee_summary = fee_summary['Senior']
        professional_fees = professional_fees['Senior']
        itemized_charges = itemized_charges['Senior']
    else:
        fee_summary = fee_summary['Regular']
        professional_fees = professional_fees['Regular']

        if patient_age < 1:
            itemized_charges = itemized_charges['Below1']
        elif patient_age >= 1 and patient_age <= 5:
            itemized_charges = itemized_charges['OneToFive']
        else:
            itemized_charges = itemized_charges['Regular']

    today_str = date.today().strftime('%b %d, %Y')

    for item_date in itemized_charges:
        item_date['date'] = today_str

    return render_template('viewPrintPDF.html', pdf_files=pdf_files,  header=statement['header'],
                           patient_info=statement['patientInfo'],
                           fee_summary=fee_summary,
                           professional_fees=professional_fees,
                           itemized_charges=itemized_charges,
                           philhealth_amount=5850.00)


def load_json(filename):
    with open(filename, 'r') as f:
        print()
        return json.load(f)


def calculate_age_month_days(date_str):
    # Convert string to date object
    year, month, day = map(int, date_str.split('-'))
    birth_date = date(year, month, day)
    today = date.today()

    # Initial difference
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    # Adjust if days are negative
    if days < 0:
        months -= 1
        # Get days in previous month
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1

        from calendar import monthrange
        days += monthrange(prev_year, prev_month)[1]

    # Adjust if months are negative
    if months < 0:
        years -= 1
        months += 12

    return f"{years} year(s) {months} months {days} days"


def calculate_age(date_str):
    # Convert string to date object
    year, month, day = map(int, date_str.split('-'))
    birth_date = date(year, month, day)
    today = date.today()

    # Calculate years
    # This checks if the current date is before the birthday in the current year
    age = today.year - birth_date.year - \
        ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age


def format_datetime(dt_string):

    if not dt_string:
        return ""
    # Convert string to datetime object
    dt = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S")

    # Format to desired output
    return dt.strftime("%B %d, %Y %H:%M:%S")


@app.route("/reports")
def view_reports():
    return render_template('reports.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
