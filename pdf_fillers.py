import os
from datetime import datetime
from flask import current_app
from fillpdf import fillpdfs
from pdf_utils import get_next_date, get_today, split_pin, spacing


def fill_cf1(data):
    pdf_path = os.path.join(current_app.root_path, "template_cf1.pdf")
    output_pdf = os.path.join(current_app.root_path, "static", "pdfs", "output_cf1.pdf")
    today = get_today()

    try:
        form_fields_cf1 = list(fillpdfs.get_form_fields(pdf_path).keys())
        patients_pin = split_pin(data['pin'])
        patients_pin[0] = spacing(patients_pin[0])
        patients_pin[1] = spacing(patients_pin[1])
        birthDate = data['dob'].split('-')

        memberMale = "Yes_xqqa" if data['sex'].lower() == "male" else None
        memberFemale = "Yes_nnyk" if data['sex'].lower() == "female" else None

        depPin = ["", "", ""]
        depDob = ["", "", ""]
        depLname = depFname = depExt = depMname = depMale = depFemale = depChild = depParent = depSpouse = isNotMember = ""
        isMember = "Yes_ofjv"

        if data.get('patientIsMember') == "no":
            isMember = None
            isNotMember = "Yes_mkfk"
            dep = data.get("dependent", {})
            depPin_value = dep.get('depPin')
            depPin = split_pin(depPin_value) if depPin_value else ["", "", ""]
            depLname = dep.get('depLname')
            depFname = dep.get('depFname')
            depExt = dep.get('depExt')
            depMname = dep.get('depMname')
            depDob_value = dep.get('depDob')
            depDob = depDob_value.split('-') if depDob_value else ["", "", ""]
            depSex_value = dep.get('depSex', '')
            depMale = "Yes_xqqa" if depSex_value.lower() == "male" else None
            depFemale = "Yes_nnyk" if depSex_value.lower() == "female" else None
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
        memberSignDate = [f"{today.month:02}", f"{today.day:02}", today.year]
        repSignDate = ["", "", ""]

        if data.get('signee', '').lower() == "representative":
            isRepresentative = "Yes_xqqa"
            signMember = None
            memberPrintedName = ""
            memberSignDate = ["", "", ""]
            rep = data.get('representative', {})
            repPrintedName = rep.get('repName')
            repSignDate = [f"{today.month:02}", f"{today.day:02}", today.year]
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
            form_fields_cf1[form_fields_cf1.index("municipality")]: data['municipality'].upper(),
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
            form_fields_cf1[form_fields_cf1.index("memberDateSignedMonth")]: "01",
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
            form_fields_cf1[form_fields_cf1.index("repOtherReasons")]: repOther,
        }

        fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data_dict)
    except Exception as e:
        print(f"This is the error {e}")


def fill_cf2(data):
    try:
        pdf_path = os.path.join(current_app.root_path, "template_cf2.pdf")
        output_pdf = os.path.join(current_app.root_path, "static", "pdfs", "output_cf2.pdf")
        form_fields_cf2 = list(fillpdfs.get_form_fields(pdf_path).keys())
        next_date = get_next_date().split('-')

        PAN = "E08039067"
        HCIName = "BURAUEN MUNICIPAL HEALTH OFFICE ANIMAL BITE TREATMENT CENTER"
        HCIAddress = "LGU COMPOUND, DISTRICT 7"
        HCIMunicipality = "BURAUEN"
        HCIProvince = "LEYTE"
        ICD10Code = "T14.1\nW55"
        RelatedProcedures = "ANIMAL BITE\nTREATMENT"
        RVSCode = "P90375"
        Doctor = "MA. QUEENA JOVE Q. SERRANO MD"
        Designation = "PHYSICIAN"
        GrandTotal = "P 5,850.00"
        AccreditationNo = ["1100", "1945935", "3"]

        today = get_today()
        date_admitted = [f"{today.month:02}", f"{today.day:02}", today.year]
        date_signed = [f"{today.month:02}", f"{today.day:02}", today.year]

        patientFname = data["firstName"].upper()
        patientMname = data["middleName"].upper()
        patientLname = data["lastName"].upper()
        patientExt = data["nameExt"].upper()

        if data["patientIsMember"] == "no":
            patientFname = data["dependent"]["depFname"]
            patientMname = data["dependent"]["depMname"]
            patientLname = data["dependent"]["depLname"]
            patientExt = data["dependent"]["depExt"]

        dispositionImprove = dispositionRecovered = dispositionHomeDischarged = dispositionAbsconded = dispositionExpired = dispositionTransferred = ""

        match (data["patientDisposition"]):
            case "Improved":
                dispositionImprove = "Yes_vzps"
            case "Recovered":
                dispositionRecovered = "Yes_vzps"
            case "HomeDischarged":
                dispositionHomeDischarged = "Yes_vzps"
            case "Absconded":
                dispositionAbsconded = "Yes_vzps"
            case "Expired":
                dispositionExpired = "Yes_vzps"
            case "Transferred":
                dispositionTransferred = "Yes_vzps"

        memberMiddleI = data.get('middleName', '')
        consentFormName = f"{data.get('firstName', '').upper()} {memberMiddleI[0].upper() + '.' if memberMiddleI else ''} {data.get('lastName', '').upper()} {data.get('nameExt', '')}".strip()
        repRelationChild = repRelationSpouse = repRelationSibling = repRelationParent = repRelationOthers = repOther = repIncapcitated = ""

        if data.get('signee', '').lower() == "representative":
            consentFormName = data["representative"]["repName"]
            repRel_value = data["representative"]["repRelationship"]
            match repRel_value.lower():
                case "spouse":
                    repRelationSpouse = "Yes_cdvw"
                case "child":
                    repRelationChild = "Yes_cdvw"
                case "sibling":
                    repRelationSibling = "Yes_cdvw"
                case "parent":
                    repRelationParent = "Yes_cdvw"
                case "others":
                    repRelationOthers = "Yes_cdvw"
            repReason = data["representative"]["repReason"].lower()
            if repReason == "others":
                repOther = "Yes_cdvw"
            else:
                repIncapcitated = "Yes_cdvw"

        data_dict_cf2 = {
            form_fields_cf2[form_fields_cf2.index("checkbox_12ekrw")]: "",
            form_fields_cf2[form_fields_cf2.index("PAN")]: PAN,
            form_fields_cf2[form_fields_cf2.index("HCIName")]: HCIName,
            form_fields_cf2[form_fields_cf2.index("HCIAddress")]: HCIAddress,
            form_fields_cf2[form_fields_cf2.index("HCIMunicipality")]: HCIMunicipality,
            form_fields_cf2[form_fields_cf2.index("HCIProvince")]: HCIProvince,
            form_fields_cf2[form_fields_cf2.index("PatientLName")]: patientLname,
            form_fields_cf2[form_fields_cf2.index("PatientFName")]: patientFname,
            form_fields_cf2[form_fields_cf2.index("PatientExt")]: patientExt,
            form_fields_cf2[form_fields_cf2.index("PatientMName")]: patientMname,
            form_fields_cf2[form_fields_cf2.index("isRefferedHCINO")]: "Yes_vzps",
            form_fields_cf2[form_fields_cf2.index("DateAdmittedMonth")]: date_admitted[0],
            form_fields_cf2[form_fields_cf2.index("DateAdmittedDay")]: date_admitted[1],
            form_fields_cf2[form_fields_cf2.index("DateAdmittedYear")]: date_admitted[2],
            form_fields_cf2[form_fields_cf2.index("DispositionImproved")]: dispositionImprove,
            form_fields_cf2[form_fields_cf2.index("DispositionExpired")]: dispositionExpired,
            form_fields_cf2[form_fields_cf2.index("DispositionRecovered")]: dispositionRecovered,
            form_fields_cf2[form_fields_cf2.index("DispositionTransferred")]: dispositionTransferred,
            form_fields_cf2[form_fields_cf2.index("DispositionHome")]: dispositionHomeDischarged,
            form_fields_cf2[form_fields_cf2.index("DispositionAbsconded")]: dispositionAbsconded,
            form_fields_cf2[form_fields_cf2.index("AccomodationNonPrivate")]: "Yes_vzps",
            form_fields_cf2[form_fields_cf2.index("Admission Diagnosis")]: "ANIMAL BITE TREATMENT",
            form_fields_cf2[form_fields_cf2.index("ICD10")]: ICD10Code,
            form_fields_cf2[form_fields_cf2.index("RelatedProcedure")]: RelatedProcedures,
            form_fields_cf2[form_fields_cf2.index("RVSCode1")]: RVSCode,
            form_fields_cf2[form_fields_cf2.index("DateProcedure")]: f"{date_admitted[0]}- \t\t -{date_admitted[2]}\n\n{next_date[0]}- \t\t -{next_date[2]}",
            form_fields_cf2[form_fields_cf2.index("Day0ARV")]: f"{date_admitted[0]}- \t\t -{date_admitted[2]}",
            form_fields_cf2[form_fields_cf2.index("RVSCode2")]: RVSCode,
            form_fields_cf2[form_fields_cf2.index("text_43ecxb")]: consentFormName,
            form_fields_cf2[form_fields_cf2.index("AccreditationNo0")]: AccreditationNo[0],
            form_fields_cf2[form_fields_cf2.index("AccreditationNo1")]: AccreditationNo[1],
            form_fields_cf2[form_fields_cf2.index("AccreditationNo2")]: AccreditationNo[2],
            form_fields_cf2[form_fields_cf2.index("AccreditationProfessional")]: Doctor,
            form_fields_cf2[form_fields_cf2.index("NoCoCopy")]: "Yes_vzps",
            form_fields_cf2[form_fields_cf2.index("AccreditationSignedMonth")]: date_signed[0],
            form_fields_cf2[form_fields_cf2.index("AccreditationSignedDay")]: "",
            form_fields_cf2[form_fields_cf2.index("AccreditationSignedYear")]: date_signed[2],
            form_fields_cf2[form_fields_cf2.index("ConsumptionBenefit1")]: "Yes_vzps",
            form_fields_cf2[form_fields_cf2.index("GrandTotal")]: GrandTotal,
            form_fields_cf2[form_fields_cf2.index("MemberDateSignMonth")]: date_signed[0],
            form_fields_cf2[form_fields_cf2.index("MemberDateSignDay")]: "",
            form_fields_cf2[form_fields_cf2.index("MemberDateSignYear")]: date_signed[2],
            form_fields_cf2[form_fields_cf2.index("RelationshipSpouse")]: repRelationSpouse,
            form_fields_cf2[form_fields_cf2.index("RelationshipChild")]: repRelationChild,
            form_fields_cf2[form_fields_cf2.index("RelationshipParent")]: repRelationParent,
            form_fields_cf2[form_fields_cf2.index("RelationshipSibling")]: repRelationSibling,
            form_fields_cf2[form_fields_cf2.index("RelationshipOthers")]: repRelationOthers,
            form_fields_cf2[form_fields_cf2.index("ReasonIncapacitated")]: repIncapcitated,
            form_fields_cf2[form_fields_cf2.index("ReasonOthers")]: repOther,
            form_fields_cf2[form_fields_cf2.index("AuthorizedHCISign")]: Doctor,
            form_fields_cf2[form_fields_cf2.index("Designation")]: Designation,
            form_fields_cf2[form_fields_cf2.index("AuthorizedSignMonth")]: date_signed[0],
            form_fields_cf2[form_fields_cf2.index("AuthorizedSignDay")]: "",
            form_fields_cf2[form_fields_cf2.index("AuthorizedSignYear")]: date_signed[2],
        }

        fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data_dict_cf2)
    except Exception as e:
        print(f"This is the error {e}")


def fill_csf(data):
    pdf_path = os.path.join(current_app.root_path, "template_csf.pdf")
    output_pdf = os.path.join(current_app.root_path, "static", "pdfs", "output_csf.pdf")
    form_fields_csf = list(fillpdfs.get_form_fields(pdf_path).keys())
    patients_pin = split_pin(data['pin'])
    birthDate = data['dob'].split('-')
    doctor = "MA. QUEENA JOVE Q. SERRANO MD"
    memberMale = "Yes_xqqa" if data['sex'].lower() == "male" else None
    memberFemale = "Yes_xqqa" if data['sex'].lower() == "female" else None
    dep_pin = ["", "", ""]
    dep_bd = ["", "", ""]
    depChild = depParent = depSpouse = ""
    depLname = data["lastName"].upper()
    depFname = data["firstName"].upper()
    depExt = data["nameExt"].upper()
    depMname = data["middleName"].upper()

    if data["dependent"]:
        dep_pin = split_pin(data["dependent"]["depPin"])
        dep_bd = data["dependent"]["depDob"].split("-")
        relationship_value = data["dependent"]["relationship"].lower()
        depLname = data['dependent']['depLname'].upper()
        depFname = data['dependent']['depFname'].upper()
        depExt = data['dependent']['depExt'].upper()
        depMname = data['dependent']['depMname'].upper()

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
    memberSignDate = [f"{get_today().month:02}", f"{get_today().day:02}", get_today().year]
    repSignDate = ["", "", ""]
    consentName = memberPrintedName
    consentIsRepresentativeSign = ""
    consentIsMemberSign = "Yes_ltey"

    if data.get('signee', '').lower() == "member" and data.get('patientIsMember', '') == "yes":
        consentIsMemberSign = "Yes_ltey"

    if data.get('signee', '').lower() == "representative":
        isRepresentative = "Yes_ltey"
        consentIsRepresentativeSign = "Yes_ltey"
        signMember = None
        memberPrintedName = ""
        memberSignDate = ["", "", ""]
        consentIsMemberSign = ""
        rep = data.get('representative', {})
        repPrintedName = rep.get('repName')
        consentName = repPrintedName
        repSignDate = [f"{get_today().month:02}", f"{get_today().day:02}", get_today().year]
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

        repReason_value = rep.get('reReason', '').lower()
        if repReason_value == "others":
            repOther = "Yes_xqqa"
        else:
            repIncapacitated = "Yes_xqqa"

    date_admitted = [f"{get_today().month:02}", f"{get_today().day:02}", get_today().year]

    data_dict_csf = {
        form_fields_csf[form_fields_csf.index("lastName")]: data["lastName"].upper(),
        form_fields_csf[form_fields_csf.index("firstName")]: data["firstName"].upper(),
        form_fields_csf[form_fields_csf.index("nameExtension")]: data["nameExt"].upper(),
        form_fields_csf[form_fields_csf.index("middleName")]: data["middleName"].upper(),
        form_fields_csf[form_fields_csf.index("pin0")]: patients_pin[0],
        form_fields_csf[form_fields_csf.index("pin1")]: patients_pin[1],
        form_fields_csf[form_fields_csf.index("pin2")]: patients_pin[2],
        form_fields_csf[form_fields_csf.index("dobMonth")]: birthDate[1],
        form_fields_csf[form_fields_csf.index("dobDay")]: birthDate[2],
        form_fields_csf[form_fields_csf.index("dobYear")]: birthDate[0],
        form_fields_csf[form_fields_csf.index("dependentLastName")]: depLname,
        form_fields_csf[form_fields_csf.index("dependentFirstName")]: depFname,
        form_fields_csf[form_fields_csf.index("dependentNameExtension")]: depExt,
        form_fields_csf[form_fields_csf.index("dependentMiddleName")]: depMname,
        form_fields_csf[form_fields_csf.index("dependentPin0")]: dep_pin[0] if dep_pin else "",
        form_fields_csf[form_fields_csf.index("dependentPin1")]: dep_pin[1] if dep_pin else "",
        form_fields_csf[form_fields_csf.index("dependentPin2")]: dep_pin[2] if dep_pin else "",
        form_fields_csf[form_fields_csf.index("patientDOBMonth")]: dep_bd[1] if dep_bd[1] else birthDate[1],
        form_fields_csf[form_fields_csf.index("patientDOBDay")]: dep_bd[2] if dep_bd[2] else birthDate[2],
        form_fields_csf[form_fields_csf.index("patientDOBYear")]: dep_bd[0] if dep_bd[0] else birthDate[0],
        form_fields_csf[form_fields_csf.index("depRelationsipChild")]: depChild,
        form_fields_csf[form_fields_csf.index("depRelationshipParent")]: depParent,
        form_fields_csf[form_fields_csf.index("depRelationshipSpouse")]: depSpouse,
        form_fields_csf[form_fields_csf.index("confineDateMonth")]: date_admitted[0],
        form_fields_csf[form_fields_csf.index("confineDateDay")]: date_admitted[1],
        form_fields_csf[form_fields_csf.index("confineDateYear")]: date_admitted[2],
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
        form_fields_csf[form_fields_csf.index("dateSignedMonth")]: memberSignDate[0],
        form_fields_csf[form_fields_csf.index("dateSignedDay")]: memberSignDate[1],
        form_fields_csf[form_fields_csf.index("dateSignedYear")]: memberSignDate[2],
        form_fields_csf[form_fields_csf.index("repDateSignedMonth")]: repSignDate[0],
        form_fields_csf[form_fields_csf.index("repDateSignedDay")]: repSignDate[1],
        form_fields_csf[form_fields_csf.index("repDateSignedYear")]: repSignDate[2],
        form_fields_csf[form_fields_csf.index("consentDateMonth")]: f"{get_today().month:02}",
        form_fields_csf[form_fields_csf.index("consentDateDay")]: f"{get_today().day:02}",
        form_fields_csf[form_fields_csf.index("consentDateYear")]: get_today().year,
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
        form_fields_csf[form_fields_csf.index("healthCareSignedMonth")]: f"{get_today().month:02}",
        form_fields_csf[form_fields_csf.index("healthCareSignedDay")]: "",
        form_fields_csf[form_fields_csf.index("healthCareSignedYear")]: get_today().year,
        form_fields_csf[form_fields_csf.index("RVSCode")]: "P90375",
        form_fields_csf[form_fields_csf.index("authHCI")]: doctor,
        form_fields_csf[form_fields_csf.index("Designation")]: "PHYSICIAN",
        form_fields_csf[form_fields_csf.index("providerSignedMonth")]: f"{get_today().month:02}",
        form_fields_csf[form_fields_csf.index("providerSignedDay")]: "",
        form_fields_csf[form_fields_csf.index("providerSignedYear")]: get_today().year,
    }

    fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data_dict_csf)


def fill_soa(data):
    pdf_path = os.path.join(current_app.root_path, "template_soa.pdf")
    output_pdf = os.path.join(current_app.root_path, "static", "pdfs", "output_soa.pdf")
    form_fields_soa = list(fillpdfs.get_form_fields(pdf_path).keys())
    now = datetime.now()
    formatted_date = now.strftime("%m-%d-%Y")
    birth_date = datetime.strptime(data.get('dob'), "%Y-%m-%d")
    today = datetime.strptime(formatted_date, "%m-%d-%Y")
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

    address = f"{data.get('street', '')} {data.get('barangay','')}, {data.get('municipality','')}, Leyte"

    if data.get('signee', '') == 'representative':
        signatory = data['representative']['repName']

    data_dict_soa = {
        form_fields_soa[0]: patientName,
        form_fields_soa[1]: formatted_date,
        form_fields_soa[2]: age,
        form_fields_soa[3]: address,
        form_fields_soa[4]: "P90375",
        form_fields_soa[6]: signatory,
    }

    fillpdfs.write_fillable_pdf(pdf_path, output_pdf, data_dict_soa)
