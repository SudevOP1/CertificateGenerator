import jinja2, pdfkit, datetime

context = {
    "name": "Sudev",
    "now" : datetime.datetime.now(),
}
pdfkit_exe_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

template_loader = jinja2.FileSystemLoader("./")
template_env = jinja2.Environment(loader=template_loader)
my_template = template_env.get_template("pdfTemplate.html")
output_text = my_template.render(context)

config = pdfkit.configuration(wkhtmltopdf=pdfkit_exe_path)
pdfkit.from_string(output_text, "generated_pdf.pdf", configuration=config)