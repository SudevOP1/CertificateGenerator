import qrcode

qrcode_text      = "Yo! This is a QR🤯"
output_file_name = "output.png"
fill_color       = "#000000" # black
back_color       = "#ffffff" # white

qr_creater = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=10,
    border=0,
)
qr_creater.add_data(qrcode_text)
qr_creater.make(fit=True)
img = qr_creater.make_image(fill_color=fill_color, back_color=back_color)

img.save(output_file_name)