import os
from datetime import date, datetime, timedelta


def get_today():
    return date.today()


def get_next_date(date_value=None):
    if date_value is None:
        date_value = datetime.today().date()

    weekday = date_value.weekday()  # Monday=0 ... Sunday=6

    if weekday <= 2:
        target_weekday = 3  # Thursday
    else:
        target_weekday = 0  # Monday

    days_ahead = (target_weekday - weekday + 7) % 7
    if days_ahead == 0:
        days_ahead = 7

    next_date = date_value + timedelta(days=days_ahead)
    return next_date.strftime("%m-%d-%Y")


def split_pin(pin_str):
    pin_str = str(pin_str).strip()

    if len(pin_str) != 12:
        raise ValueError("PIN must be at least 3 digits.")

    first_two = pin_str[:2]
    last_digit = pin_str[-1]
    middle = pin_str[2:-1]

    return [first_two, middle, last_digit]


def spacing(data):
    new_data = " "
    i = 2
    for letter in data:
        if i % 2 == 0:
            new_data += letter + "  "
        else:
            new_data += letter + "   "
        i += 1
    return new_data


def clean_files(file_list, root_path):
    for f in file_list:
        try:
            path = os.path.join(root_path, "static", "pdfs", f)
            if os.path.exists(path):
                os.remove(path)
                print(f"Deleted {f}")
        except Exception as e:
            print(f"Error deleting {f}: {e}")


def merge_pdfs(pdf_list, output_pdf):
    from PyPDF2 import PdfMerger

    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_pdf)
    merger.close()
    print(f"Merged PDF saved as {output_pdf}")
