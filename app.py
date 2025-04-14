from flask import Flask, render_template_string, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
import datetime
from sheetUtil import append_to_google_sheet

app = Flask(__name__)

form_html = """
<!doctype html>
<title>Patient Form</title>
<h2>Enter Patient Details</h2>
<form method="post">
    Patient Name: <input type="text" name="patient_name" required><br><br>
    Age: <input type="text" name="age" required><br><br>
    Gender: <select name="gender" required>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
           </select><br><br>
    Slip Note & Time: <input type="text" name="slip_note_time" value="{{ time }}" required><br><br>
    Doctor Name: <input type="text" name="doctor_name" required><br><br>
    Created By: <input type="text" name="created_by" required><br><br>
    <input type="submit" value="Generate PDF">
</form>
"""

def generate_prescription(data, token_number):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFillColor(colors.lightgrey)
    c.rect(0, height - 60, width, 40, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(170, height - 45, "ORTHOCARE Hospital By Pradeep")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, height - 70, "MR# 1")
    
    # Dynamically set the token number
    c.drawString((width / 2) - 20, height - 70, f"TOKEN# {token_number}")
    c.drawString(width - 70, height - 70, "OPD - 1")

    c.setFont("Helvetica", 10)
    top = height - 80
    c.rect(30, top - 60, width - 60, 55)
    c.drawString(40, top - 20, f"Patient Name: {data['patient_name']}")
    c.drawString(300, top - 20, f"Age: {data['age']}   Gender: {data['gender']}")
    c.drawString(40, top - 35, f"Slip Note & Time: {data['slip_note_time']}")
    c.drawString(300, top - 35, f"Created By: {data['created_by']}")
    c.drawString(40, top - 50, f"Doctor Name: {data['doctor_name']}")

    body_top = top - 70
    body_height = 400
    c.rect(30, body_top - body_height, width - 60, body_height)

    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.line(160, body_top, 160, body_top - body_height)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, body_top - 30, "Vitals")

    c.setFont("Helvetica", 10)
    investigations = [
        "☐ Blood CP",
        "☐ Urine R/E",
        "☐ RFT",
        "☐ LFT",
        "☐ U/S Kub Abd",
        "☐ U/S Pelvis Postvoid",
        "☐ ECG"
    ]
    y = body_top - 50
    for item in investigations:
        c.drawString(40, y, item)
        y -= 15

    c.setFont("Helvetica-Bold", 12)
    c.drawString(180, body_top - 30, "Prescription")

    c.setFont("Helvetica-BoldOblique", 30)
    c.drawString(170, body_top - 70, "Rx")

    c.rect(30, 60, width - 60, 40)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 75, "Note: ............................................................................................................................")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.to_dict()
        token_number = append_to_google_sheet(data)  # Get the token number after appending to Google Sheets
        pdf_file = generate_prescription(data, token_number)  # Pass both data and token_number to the PDF generation function
        filename = f"{data['patient_name'].replace(' ', '_')}_prescription.pdf"
        return send_file(pdf_file, as_attachment=True, download_name=filename)

    # For GET request
    current_time = datetime.datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
    return render_template_string(form_html, time=current_time)
if __name__ == "__main__":
    app.run(debug=True)
