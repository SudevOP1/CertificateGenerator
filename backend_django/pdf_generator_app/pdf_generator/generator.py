import jinja2, pdfkit, os, base64

base_path = os.path.dirname(os.path.abspath(__file__))
template_file_name = "template.html"
template_file_path = base_path  # path to the current folder

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
        "badge_path":       badge_path,
        "attendee_name":    attendee_name,
        "attendee_email":   attendee_email,
    }

    rendered_html = my_template.render(context)
    # creating pdf in memory:
    pdf_bytes = pdfkit.from_string(rendered_html, False, configuration=config, options={'enable-local-file-access': None})
    # encoding pdf:
    encoded_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    return encoded_pdf