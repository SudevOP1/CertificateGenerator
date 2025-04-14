import jinja2, pdfkit, datetime

context = {
    "name": "Sudev",
    "now" : datetime.datetime.now(),
}
output_file_name    = "output.pdf"
template_file_name  = "template.html"
template_file_path  = "./"
pdfkit_exe_path     = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

template_loader = jinja2.FileSystemLoader(template_file_path)
template_env = jinja2.Environment(loader=template_loader)
my_template = template_env.get_template(template_file_name)
output_text = my_template.render(context)

config = pdfkit.configuration(wkhtmltopdf=pdfkit_exe_path)
pdfkit.from_string(output_text, output_file_name, configuration=config)