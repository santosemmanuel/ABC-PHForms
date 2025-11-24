from flask import Flask, render_template, request, jsonify
from fillpdf import fillpdfs
from pdfrw import PdfReader as PdfRwReader, PdfWriter as PdfRwWriter, PageMerge, PdfDict, PdfName
from datetime import datetime, date
from pdf2image import convert_from_path
# import img2pdf
import os
import json

# Initialize Flask app
app = Flask(__name__)
    
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

today = date.today()

def flatten_pdf(input_pdf, output_pdf):
    pdf = PdfRwReader(input_pdf)
    for page in pdf.pages:
        annots = page.get(PdfName('Annots'))
        if not annots:
            continue
        for annot in annots:
            subtype = annot.get(PdfName('Subtype'))
            if subtype != PdfName('Widget'):
                continue
            ap = annot.get(PdfName('AP'))
            if not isinstance(ap, PdfDict):
                continue
            n_ap = ap.get(PdfName('N'))
            if n_ap and hasattr(n_ap, 'stream'):
                try:
                    PageMerge(page).add(n_ap).render()
                except Exception as e:
                    print("Skipping annotation:", e)
        # Remove annotations so fields become static drawings
        page[PdfName('Annots')] = []
    PdfRwWriter().write(output_pdf, pdf)
    print(f"Flattened PDF saved as {output_pdf}")

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
    fill_csf(patient_data)
    fill_soa(patient_data)
    # Debug: see the data received
    # TODO: Save to database or process
   
    # Merge all flattened PDFs
    merge_pdfs(["output_cf1.pdf", "output_csf.pdf", "output_soa.pdf"], "final_merged.pdf")

    # Optional: delete individual PDFs
    #clean_files(["output_cf1.pdf", "output_csf.pdf", "output_soa.pdf"])

    return jsonify({"status": "success", "message": "Form received"})

def fill_cf1(data):

    output_pdf = 'output_cf1.pdf'
    pdf_path = "template_cf1.pdf"

    try:
        form_fields_cf1 = list(fillpdfs.get_form_fields(pdf_path).keys())
        patients_pin = data['pin'].split('-')
        birthDate = data['dob'].split('-')

        memberMale = "Yes_xqqa" if data['sex'].lower() == "male" else None
        memberFemale = "Yes_xqqa" if data['sex'].lower() == "female" else None

        depPin = ["", "", ""]
        depDob = ["", "", ""]
        depLname = depFname = depExt = depMname = depMale = depFemale = depChild = depParent = depSpouse = isNotMember = ""
        isMember = "Yes_ofjv"

        if data.get('patientIsMember') == "no":
            isMember = None
            isNotMember = "Yes_mkfk"

            dep = data.get("dependent", {})

            # Safe PIN
            depPin_value = dep.get('depPin')
            depPin = depPin_value.split('-') if depPin_value else ["", "", ""]

            depLname = dep.get('depLname')
            depFname = dep.get('depFname')
            depExt = dep.get('depExt')
            depMname = dep.get('depMname')

            # Safe DOB
            depDob_value = dep.get('depDob')
            depDob = depDob_value.split('-') if depDob_value else ["", "", ""]

            # Sex
            depSex_value = dep.get('depSex', '')
            depMale = "Yes_xqqa" if depSex_value.lower() == "male" else None
            depFemale = "Yes_nnyk" if depSex_value.lower() == "female" else None

            # Relationship
            relationship_value = dep.get('relationship', '').lower()

            match relationship_value:
                case "child":
                    depChild = "Yes_xqqa"
                case "parent":
                    depParent = "Yes_xqqa"
                case "spouse":
                    depSpouse = "Yes_xqqa"

        isRepresentative = repPrintedName = repRelationSpouse = repRelationChild = repRelationSibling = repRelationParent = repRelationOthers = repOther = repIncapacitated = ""
        signMember = "Yes_xqqa"

        memberMiddleI = data.get('middleName', '')
        memberPrintedName = f"{data.get('firstName', '').upper()} {memberMiddleI[0].upper() + '.' if memberMiddleI else ''} {data.get('lastName', '').upper()} {data.get('nameExt', '')}".strip()
        memberSignDate = [today.month, today.day, today.year]
        repSignDate = ["", "", ""]

        if data.get('signee', '').lower() == "representative":
            isRepresentative = "Yes_xqqa"
            signMember = None
            memberPrintedName = ""
            memberSignDate = ["", "", ""]

            rep = data.get('representative', {})
            repPrintedName = rep.get('repName')
            repSignDate = [today.month, today.day, today.year]

            repRel_value = rep.get('repRelationship', '').lower()

            match repRel_value:
                case "spouse":
                    repRelationSpouse = "Yes_xqqa"
                case "child":
                    repRelationChild = "Yes_xqqa"
                case "sibling":
                    repRelationSibling = "Yes_xqqa"
                case "parent":
                    repRelationParent = "Yes_xqqa"
                case "others":
                    repRelationOthers = "Yes_xqqa"

            # Reason
            repReason_value = rep.get('reReason', '').lower()

            if repReason_value == "others":
                repOther = "Yes_xqqa"
            else:
                repIncapacitated = "Yes_xqqa"


        data_dict = {
            form_fields_cf1[form_fields_cf1.index("pin0")]: patients_pin[0],
            form_fields_cf1[form_fields_cf1.index("pin1")]: patients_pin[1],
            form_fields_cf1[form_fields_cf1.index("pin2")]: patients_pin[2],
            form_fields_cf1[form_fields_cf1.index("lastName")]: data['lastName'].upper(),
            form_fields_cf1[form_fields_cf1.index("firstName")]: data['firstName'].upper(),
            form_fields_cf1[form_fields_cf1.index("nameExtension")]: data['nameExt'],
            form_fields_cf1[form_fields_cf1.index("middleName")]: data['middleName'].upper(),
            form_fields_cf1[form_fields_cf1.index("dobMonth")]: birthDate[1],
            form_fields_cf1[form_fields_cf1.index("dobDay")]: birthDate[2],
            form_fields_cf1[form_fields_cf1.index("dobYear")]: birthDate[0],
            form_fields_cf1[form_fields_cf1.index("memberMale")]: memberMale,
            form_fields_cf1[form_fields_cf1.index("memberFemale")]: memberFemale,
            form_fields_cf1[form_fields_cf1.index("street")]: data['street'],
            form_fields_cf1[form_fields_cf1.index("barangay")]: data['barangay'].upper(),
            form_fields_cf1[form_fields_cf1.index("municipality")]: "BURAUEN",
            form_fields_cf1[form_fields_cf1.index("province")]: "LEYTE",
            form_fields_cf1[form_fields_cf1.index("country")]: "PHILLIPPINES",
            form_fields_cf1[form_fields_cf1.index("zipcode")]: "6516",
            form_fields_cf1[form_fields_cf1.index("mobileNumber")]: data['mobile'],
            form_fields_cf1[form_fields_cf1.index("emailAddress")]: data['email'],
            form_fields_cf1[form_fields_cf1.index("isMember")]: isMember,
            form_fields_cf1[form_fields_cf1.index("isNotMember")]: isNotMember,

            form_fields_cf1[form_fields_cf1.index("dependentPIN0")]: depPin[0],
            form_fields_cf1[form_fields_cf1.index("dependentPIN1")]: depPin[1],
            form_fields_cf1[form_fields_cf1.index("dependentPIN2")]: depPin[2],
            form_fields_cf1[form_fields_cf1.index("dependentLastName")]: (depLname or "").upper(),
            form_fields_cf1[form_fields_cf1.index("dependentFirstName")]: (depFname or "").upper(),
            form_fields_cf1[form_fields_cf1.index("dependentNameExtension")]: (depExt or "").upper(),
            form_fields_cf1[form_fields_cf1.index("dependentMiddleName")]: (depMname or "").upper(),
            form_fields_cf1[form_fields_cf1.index("dependentDOBMonth")]: depDob[1],
            form_fields_cf1[form_fields_cf1.index("dependentDOBDay")]: depDob[2],
            form_fields_cf1[form_fields_cf1.index("dependentDOBYear")]: depDob[0],
            form_fields_cf1[form_fields_cf1.index("relationshipChild")]: depChild,
            form_fields_cf1[form_fields_cf1.index("relationshipParent")]: depParent,
            form_fields_cf1[form_fields_cf1.index("relationshipSpouse")]: depSpouse,
            form_fields_cf1[form_fields_cf1.index("dependentMale")]: depMale,
            form_fields_cf1[form_fields_cf1.index("dependentFemale")]: depFemale,

            form_fields_cf1[form_fields_cf1.index("memberCertSignature")]: memberPrintedName,
            form_fields_cf1[form_fields_cf1.index("memberCertRepSignature")]: repPrintedName,

            form_fields_cf1[form_fields_cf1.index("memberDateSignedMonth")]: memberSignDate[0],
            form_fields_cf1[form_fields_cf1.index("memberDateSignedDay")]: memberSignDate[1],
            form_fields_cf1[form_fields_cf1.index("memberDateSignedYear")]: memberSignDate[2],

            form_fields_cf1[form_fields_cf1.index("repDateSginedMonth")]: repSignDate[0],
            form_fields_cf1[form_fields_cf1.index("repDateSginedDay")]: repSignDate[1],
            form_fields_cf1[form_fields_cf1.index("repDateSginedYear")]: repSignDate[2],

            form_fields_cf1[form_fields_cf1.index("repRelationSpouse")]: repRelationSpouse,
            form_fields_cf1[form_fields_cf1.index("repRelationChild")]: repRelationChild,
            form_fields_cf1[form_fields_cf1.index("repRelationParent")]: repRelationParent,
            form_fields_cf1[form_fields_cf1.index("repRelationSibling")]: repRelationSibling,
            form_fields_cf1[form_fields_cf1.index("repOthers")]: repRelationOthers,
            form_fields_cf1[form_fields_cf1.index("repOtherSpecify")]: "",
            form_fields_cf1[form_fields_cf1.index("repReasonIncapacitated")]: repIncapacitated,
            form_fields_cf1[form_fields_cf1.index("memberCertMember")]: signMember,
            form_fields_cf1[form_fields_cf1.index("memberCertRepresentative")]: isRepresentative,
            form_fields_cf1[form_fields_cf1.index("repOtherReasonsReason")]: "",
            form_fields_cf1[form_fields_cf1.index("repOtherReasons")]: repOther
        }

    
        fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data_dict)
        fillpdfs.flatten_pdf(output_pdf, output_pdf, as_images=True)
    except Exception as e:
        print(f"This is the error {e}")

def fill_cf2():
    pass

def fill_csf(data):

    output_pdf = 'output_csf.pdf'
    pdf_path = "template_csf.pdf"

    form_fields_csf = list(fillpdfs.get_form_fields(pdf_path).keys())
    print(form_fields_csf)

    patients_pin = data['pin'].split('-')
    birthDate = data['dob'].split('-')

    doctor = "MA. QUEENA JOVE Q. SERRANO MD"

    memberMale = "Yes_xqqa" if data['sex'].lower() == "male" else None
    memberFemale = "Yes_xqqa" if data['sex'].lower() == "female" else None

    dep_pin = ["","",""]
    dep_bd = ["","",""]
    depChild = depParent = depSpouse = ""
    if data["dependent"]:
        dep_pin = data["dependent"]["depPin"].split("-")
        dep_bd = data["dependent"]["depDob"].split("-")

        relationship_value = data["dependent"]["relationship"].lower()

        match relationship_value:
            case "child":
                depChild = "Yes_ltey"
            case "parent":
                depParent = "Yes_ltey"
            case "spouse":
                depSpouse = "Yes_ltey"

    isRepresentative = repPrintedName = repRelationSpouse = repRelationChild = repRelationSibling = repRelationParent = repRelationOthers = repOther = repIncapacitated = ""
    signMember = "Yes_ltey"
    
    memberMiddleI = data.get('middleName', '')
    memberPrintedName = f"{data.get('firstName', '').upper()} {memberMiddleI[0].upper() + '.' if memberMiddleI else ''} {data.get('lastName', '').upper()} {data.get('nameExt', '')}".strip()
    memberSignDate = [today.month, today.day, today.year]
    repSignDate = ["", "", ""]
    consentName = memberPrintedName
    consentIsRepresentativeSign = ""
    consentIsMemberSign = ""

    if data.get('signee','').lower() == "member" and data.get('patientIsMember','') == "yes":
        consentIsMemberSign = "Yes_ltey"
    
    if data.get('signee', '').lower() == "representative":
        isRepresentative = "Yes_ltey"
        consentIsRepresentativeSign = "Yes_ltey"
        signMember = None
        memberPrintedName = ""
        memberSignDate = ["", "", ""]

        rep = data.get('representative', {})
        repPrintedName = rep.get('repName')
        consentName = repPrintedName
        repSignDate = [today.month, today.day, today.year]
        isRepresentative = "Yes_ltey"

        repRel_value = rep.get('repRelationship', '').lower()

        match repRel_value:
            case "spouse":
                repRelationSpouse = "Yes_ltey"
            case "child":
                repRelationChild = "Yes_ltey"
            case "sibling":
                repRelationSibling = "Yes_ltey"
            case "parent":
                repRelationParent = "Yes_ltey"
            case "others":
                repRelationOthers = "Yes_ltey"

        # Reason
        repReason_value = rep.get('reReason', '').lower()

        if repReason_value == "others":
            repOther = "Yes_xqqa"
        else:
            repIncapacitated = "Yes_xqqa"

    date_admitted = [today.month, today.day, today.year]

    data_dict_csf = {
        # -----------------------------
        # Patient Name
        # -----------------------------
        form_fields_csf[form_fields_csf.index("lastName")]: data["lastName"].upper(),
        form_fields_csf[form_fields_csf.index("firstName")]: data["firstName"].upper(),
        form_fields_csf[form_fields_csf.index("nameExtension")]: data["nameExt"].upper(),
        form_fields_csf[form_fields_csf.index("middleName")]: data["middleName"].upper(),

        # -----------------------------
        # Patient PIN (PhilHealth ID)
        # -----------------------------
        form_fields_csf[form_fields_csf.index("pin0")]: patients_pin[0],
        form_fields_csf[form_fields_csf.index("pin1")]: patients_pin[1],
        form_fields_csf[form_fields_csf.index("pin2")]: patients_pin[2],

        # -----------------------------
        # Patient DOB
        # -----------------------------
        form_fields_csf[form_fields_csf.index("dobMonth")]: birthDate[1],
        form_fields_csf[form_fields_csf.index("dobDay")]: birthDate[2],
        form_fields_csf[form_fields_csf.index("dobYear")]: birthDate[0],

        # -----------------------------
        # Dependent Name
        # -----------------------------
        form_fields_csf[form_fields_csf.index("dependentLastName")]: data['dependent']['depLname'].upper() if data['dependent']['depLname'] else "",
        form_fields_csf[form_fields_csf.index("dependentFirstName")]: data['dependent']['depFname'].upper() if data['dependent']['depFname'] else "",
        form_fields_csf[form_fields_csf.index("dependentNameExtension")]: data['dependent']['depExt'].upper() if data['dependent']['depExt'] else "",
        form_fields_csf[form_fields_csf.index("dependentMiddleName")]: data['dependent']['depMname'].upper() if data['dependent']['depMname'] else "",

        # # -----------------------------
        # # Dependent PIN
        # # -----------------------------
        form_fields_csf[form_fields_csf.index("dependentPin0")]: dep_pin[0] if dep_pin else "",
        form_fields_csf[form_fields_csf.index("dependentPin1")]: dep_pin[1] if dep_pin else "",
        form_fields_csf[form_fields_csf.index("dependentPin2")]: dep_pin[2] if dep_pin else "",

        form_fields_csf[form_fields_csf.index("patientDOBMonth")]: dep_bd[1] if dep_bd else "",
        form_fields_csf[form_fields_csf.index("patientDOBDay")]: dep_bd[2] if dep_bd else "",
        form_fields_csf[form_fields_csf.index("patientDOBYear")]: dep_bd[0] if dep_bd else "",

        # # -----------------------------
        # # Relationship Checkboxes
        # # These will be filled later as ✔ or blank
        # # -----------------------------
        form_fields_csf[form_fields_csf.index("depRelationsipChild")]: depChild,
        form_fields_csf[form_fields_csf.index("depRelationshipParent")]: depParent,
        form_fields_csf[form_fields_csf.index("depRelationshipSpouse")]: depSpouse,


        form_fields_csf[form_fields_csf.index("confineDateMonth")]: date_admitted[0],
        form_fields_csf[form_fields_csf.index("confineDateDay")]: date_admitted[1],
        form_fields_csf[form_fields_csf.index("confineDateYear")]: date_admitted[2],
        # # -----------------------------
        # # Representative Types / Signatures
        # # -----------------------------
        form_fields_csf[form_fields_csf.index("memberSignature")]: memberPrintedName,
        form_fields_csf[form_fields_csf.index("isMemberSignature")]: signMember,

        form_fields_csf[form_fields_csf.index("repSignature")]: repPrintedName,
        form_fields_csf[form_fields_csf.index("repDateSignedMonth")]: repSignDate[0],
        form_fields_csf[form_fields_csf.index("repDateSignedDay")]: repSignDate[1],
        form_fields_csf[form_fields_csf.index("repDateSignedYear")]: repSignDate[2],
        form_fields_csf[form_fields_csf.index("repChild")]: repRelationChild,
        form_fields_csf[form_fields_csf.index("repParent")]: repRelationParent,
        form_fields_csf[form_fields_csf.index("repSpouse")]: repRelationSpouse,
        form_fields_csf[form_fields_csf.index("repSibling")]: repRelationSibling,
        form_fields_csf[form_fields_csf.index("repOthers")]: repRelationOthers,
        # form_fields_csf[form_fields_csf.index("ifPatient")]: "",
        # form_fields_csf[form_fields_csf.index("ifRepresentative")]: "",

        # # -----------------------------
        # # Date Signed (Patient)
        # # -----------------------------
        form_fields_csf[form_fields_csf.index("dateSignedMonth")]: memberSignDate[0],
        form_fields_csf[form_fields_csf.index("dateSignedDay")]: memberSignDate[1],
        form_fields_csf[form_fields_csf.index("dateSignedYear")]: memberSignDate[2],

        # # -----------------------------
        # # Representative Date Signed
        # # -----------------------------
        form_fields_csf[form_fields_csf.index("repDateSignedMonth")]: repSignDate[0],
        form_fields_csf[form_fields_csf.index("repDateSignedDay")]: repSignDate[1],
        form_fields_csf[form_fields_csf.index("repDateSignedYear")]: repSignDate[2],

        form_fields_csf[form_fields_csf.index("consentDateMonth")]: today.month,
        form_fields_csf[form_fields_csf.index("consentDateDay")]: today.day,
        form_fields_csf[form_fields_csf.index("consentDateYear")]: today.year,
        form_fields_csf[form_fields_csf.index("repSpouse1")]: depSpouse,
        form_fields_csf[form_fields_csf.index("repChild1")]: depChild,
        form_fields_csf[form_fields_csf.index("repParent1")]: depParent,
        form_fields_csf[form_fields_csf.index("repSibling1")]: repRelationSibling,
        form_fields_csf[form_fields_csf.index("repOther1")]: repRelationOthers,

        form_fields_csf[form_fields_csf.index("SignatureMemberRep")]: consentName, 
        form_fields_csf[form_fields_csf.index("ifPatient")]: consentIsMemberSign,
        form_fields_csf[form_fields_csf.index("ifRepresentative")]: consentIsRepresentativeSign,
        
        form_fields_csf[form_fields_csf.index("accreditationNo0")]: "1100",
        form_fields_csf[form_fields_csf.index("accreditationNo1")]: "1945935",
        form_fields_csf[form_fields_csf.index("accreditationNo2")]: "3",
        form_fields_csf[form_fields_csf.index("healthCareSignature")]: doctor,
        form_fields_csf[form_fields_csf.index("healthCareSignedMonth")]: today.month,
        form_fields_csf[form_fields_csf.index("healthCareSignedDay")]: today.day,
        form_fields_csf[form_fields_csf.index("healthCareSignedYear")]: today.year,

        form_fields_csf[form_fields_csf.index("RVSCode")]: "P90375",
        form_fields_csf[form_fields_csf.index("authHCI")]: doctor,
        form_fields_csf[form_fields_csf.index("Designation")]: "PHYSICIAN",
        form_fields_csf[form_fields_csf.index("providerSignedMonth")]: today.month,
        form_fields_csf[form_fields_csf.index("providerSignedDay")]: today.day,
        form_fields_csf[form_fields_csf.index("providerSignedYear")]: today.year,       
        
    }
  
    fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data_dict_csf)
    #flatten_pdf(output_pdf, output_pdf)

def fill_soa(data):
    
    output_pdf = 'output_soa.pdf'
    pdf_path = "template_soa.pdf"

    form_fields_soa = list(fillpdfs.get_form_fields(pdf_path).keys())

    # Get the current date and time
    now = datetime.now()

    # Format the date as MM-DD-YYYY
    formatted_date = now.strftime("%m-%d-%Y")

    birth_date = datetime.strptime(data.get('dob'), "%Y-%m-%d")
    today = datetime.strptime(formatted_date, "%m-%d-%Y")

    # Calculate age
    age = today.year - birth_date.year

    
    memberMiddleI = data.get('middleName', '')
    patientName = f"{data.get('firstName', '').upper()} {memberMiddleI[0].upper() + '.' if memberMiddleI else ''} {data.get('lastName', '').upper()} {data.get('nameExt', '')}".strip()
    signatory = patientName 
    
    if data['patientIsMember'] == "no":
        memberMiddleI = data['dependent']['depMname']
        patientName = f"{data['dependent']['depFname'].upper()} {memberMiddleI[0].upper() + '.' if memberMiddleI else ''} {data['dependent']['depLname'].upper()} {data['dependent']['depExt']}".strip()
        birth_date = datetime.strptime(data['dependent']['depDob'], "%Y-%m-%d")
        age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    address = f"{data.get('street', '')} {data.get('barangay','')}, Burauen, Leyte"

    if data.get('signee','') == 'representative':
        signatory = data['representative']['repName']

    data_dict_soa = {
        form_fields_soa[0]: patientName,
        form_fields_soa[1]: formatted_date,
        form_fields_soa[2]: age,
        form_fields_soa[3]: address,
        form_fields_soa[4]: "P90375",
        form_fields_soa[6]: signatory
    }

    fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data_dict_soa)
    flatten_pdf(output_pdf, output_pdf)

def merge_pdfs(pdf_list, output_pdf):
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_pdf)
    merger.close()
    print(f"Merged PDF saved as {output_pdf}")

# def pdf_to_image_pdf(input_pdf, output_pdf):
    # Convert PDF pages to images
    # pages = convert_from_path(input_pdf)
    # image_files = []
    # for i, page in enumerate(pages):
    #     img_path = f"temp_page_{i}.png"
    #     page.save(img_path, "PNG")
    #     image_files.append(img_path)

    # # Merge images into PDF
    # with open(output_pdf, "wb") as f:
    #     f.write(img2pdf.convert(image_files))

    # # Clean temp images
    # for img in image_files:
    #     if os.path.exists(img):
    #         os.remove(img)

    # print(f"Converted {input_pdf} → {output_pdf}")
    # return output_pdf

def clean_files(file_list):
    for f in file_list:
        try:
            if os.path.exists(f):
                os.remove(f)
                print(f"Deleted {f}")
        except Exception as e:
            print(f"Error deleting {f}: {e}")

@app.route("/view_print")
def view_print_pdf():
    return render_template('viewPrintPDF.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)