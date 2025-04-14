import qrcode

qrcode_text      = "Yo! This is a QR🤯"
output_file_name = "output.png"

img = qrcode.make(qrcode_text)
img.save(output_file_name)