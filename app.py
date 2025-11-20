from flask import Flask, render_template, request, jsonify, send_file
from pdfrw import PdfReader, PdfDict
from PyPDF2 import PdfWriter
from fillpdf import fillpdfs
import json

# Initialize Flask app
app = Flask(__name__)


pdf_path = "Test.pdf"
    
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
    print(pretty_json_string)
    fill_cf1(patient_data)
    # Debug: see the data received
    # TODO: Save to database or process
    return jsonify({"status": "success", "message": "Form received"})

def fill_cf1(data):
    # reader = PdfReader(pdf_path)

    output_pdf = 'filled.pdf'
    # fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data)
    # # Send the filled PDF as a download
    # return send_file(output_pdf, as_attachment=True)
    form_fields = list(fillpdfs.get_form_fields(pdf_path).keys())
    print(form_fields)

    # data_dict = {
    #     form_fields[0]: data["lastName"]
    # }
    fields = ['untitled1', 'untitled2', 'untitled3', 'untitled4', 'untitled5', 'untitled6',
          'untitled7', 'untitled8', 'untitled9', 'untitled10', 'untitled11', 'untitled12',
          'untitled13', 'untitled14', 'untitled15', 'untitled16', 'untitled17', 'untitled18',
          'untitled19', 'untitled20', 'untitled21', 'untitled22', 'untitled23', 'untitled24',
          'untitled25', 'untitled26', 'untitled27', 'untitled28', 'untitled29', 'untitled30',
          'untitled31', 'untitled32', 'untitled33', 'untitled34', 'untitled35', 'untitled36',
          'untitled37', 'untitled38', 'untitled39', 'untitled40', 'untitled80', 'untitled81',
          'untitled82', 'untitled83', 'untitled84', 'untitled85', 'untitled86', 'untitled87',
          'untitled88', 'untitled89', 'untitled90', 'untitled91', 'untitled92', 'untitled93',
          'untitled94', 'untitled95', 'untitled0', '0', '1', '2', '3', '4', '5', '6', '7', '8',
          '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '22', '23',
          '24', '25', '26', '27', '28', '29', '30', 'Text Field0', 'Text Field1']

# Create dict with dummy values
    dummy_data = {field: f"dummy_{i}" for i, field in enumerate(fields)}
    fillpdfs.write_fillable_pdf(pdf_path, output_pdf, dummy_data)

def fill_cf2():
    pass

def fill_csf():
    pass

def fill_soa():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)