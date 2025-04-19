import jinja2, pdfkit, os, base64

base_path = os.path.dirname(os.path.abspath(__file__))
template_file_name = "template.html"
template_file_path = base_path  # path to the current folder
bg_path = f"file:///{base_path}/bg_img.png".replace(os.sep, "/")

pdfkit_exe_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

config = pdfkit.configuration(wkhtmltopdf=pdfkit_exe_path)
template_loader = jinja2.FileSystemLoader(template_file_path)
template_env = jinja2.Environment(loader=template_loader)
my_template = template_env.get_template(template_file_name)

def get_pdf_file(organizer_name, workshop_name, date, qr, attendee_name, attendee_email):
    badge_path  = f"file:///{base_path}/badge.png"

    context = {
        "organizer_name":   organizer_name,
        "workshop_name":    workshop_name,
        "date":             date,
        "qr_path":          qr,
        "bg_path":          bg_path,
        "badge_path":       badge_path,
        "attendee_name":    attendee_name,
        "attendee_email":   attendee_email,
    }

    rendered_html = my_template.render(context)
    # creating pdf in memory:
    pdf_bytes = pdfkit.from_string(
        rendered_html,
        False,
        configuration=config,
        options={
            'enable-local-file-access': None,
            'margin-top': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            'margin-right': '0mm',
            'page-width': '211.67mm',
            'page-height': '145.52mm',
            'dpi': 300,
            'zoom': 1,
        }
    )
    # encoding pdf:
    encoded_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    return encoded_pdf

if __name__ == "__main__":

    # Sample demo data
    organizer_name = "Smit Doshi"
    workshop_name = "Python in 69 Hours"
    date = "2025-01-25"
    attendee_name = "John Doe"
    attendee_email = "johndoe@example.com"
    
    sample_qr_filename = "demo_qr.png"
    qr_path = f"file:///{os.path.join(base_path, sample_qr_filename).replace(os.sep, '/')}"

    # Generate base64 PDF
    encoded_pdf = get_pdf_file(
        organizer_name=organizer_name,
        workshop_name=workshop_name,
        date=date,
        qr=qr_path,
        attendee_name=attendee_name,
        attendee_email=attendee_email,
    )

    # Decode and save as output.pdf
    pdf_bytes = base64.b64decode(encoded_pdf)
    output_path = os.path.join(base_path, "output.pdf")
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    # print(f"PDF saved to {output_path}")