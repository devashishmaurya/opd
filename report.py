from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_prescription(filename="prescription.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Header bar
    c.setFillColor(colors.lightgrey)
    c.rect(0, height - 60, width, 40, fill=1)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(170, height - 45, "ORTHOCARE Hospital By Pradeep")

      # MR#, TOKEN#, OPD info
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, height - 70, "MR# 1")
    c.drawString((width / 2) - 20, height - 70, "TOKEN# 1")
    c.drawString(width - 70, height - 70, "OPD - 1")


    # Section 1: Patient Info Box
    c.setFont("Helvetica", 10)
    top = height - 80
    c.rect(30, top - 60, width - 60, 55)  # Patient Info Box
    c.drawString(40, top - 20, "Patient Name: ...Mr. RAMENDRA MAURYA...")
    c.drawString(300, top - 20, "Age: ..33..   Gender: Male")
    c.drawString(40, top - 35, "Slip Note & Time: 19-Mar-2025 08:58:23 PM")
    c.drawString(300, top - 35, "Created By: Admin")
    c.drawString(40, top - 50, "Doctor Name: DR PRADEEP KRIPLANI (MD MBBS)")

    # Section 2: Main Body Box (Vitals + Prescription)
    body_top = top - 70
    body_height = 400
    c.rect(30, body_top - body_height, width - 60, body_height)

    # Add vertical separator between Vitals and Prescription
    c.setStrokeColor(colors.grey)
    c.setLineWidth(1)
    c.line(160, body_top, 160, body_top - body_height)

    # Vitals Section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, body_top - 30, "Vitals")

    # List of Investigations in Vitals section
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

    # Prescription section
    c.setFont("Helvetica-Bold", 12)
    c.drawString(180, body_top - 30, "Prescription")

    # Rx symbol
    c.setFont("Helvetica-BoldOblique", 30)
    c.drawString(170, body_top - 70, "Rx")

    # Footer box (Optional Note)
    c.rect(30, 60, width - 60, 40)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(40, 75, "Note: ............................................................................................................................")

    c.showPage()
    c.save()

# Run it
generate_prescription()
