import jinja2, pdfkit, datetime, os

base_path = os.path.abspath(".").replace("\\", "/")
qr_path = f"file:///{base_path}/qr.png"
badge_path = f"file:///{base_path}/badge.png"
output_file_name    = "output.pdf"
template_file_name  = "template.html"
template_file_path  = "./"
pdfkit_exe_path     = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

context = {
    "name"          : "Sudev Dahitule",
    "workshop_name" : "Python in 2 Hours",
    "date"          : datetime.date.today().strftime("%B %d, %Y"),
    "qr_path"       : qr_path,
    "badge_path"    : badge_path
}

template_loader = jinja2.FileSystemLoader(template_file_path)
template_env = jinja2.Environment(loader=template_loader)
my_template = template_env.get_template(template_file_name)
output_text = my_template.render(context)

config = pdfkit.configuration(wkhtmltopdf=pdfkit_exe_path)
pdfkit.from_string(output_text, output_file_name, configuration=config, options={'enable-local-file-access': None})