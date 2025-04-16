import qrcode, os

outputs_folder_name = "outputs"

def generate_qr(text, output_file_name, fill_color="#000000", back_color="#ffffff"):

    # create outputs folder if not present
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), outputs_folder_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, output_file_name)

    qr_creator = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr_creator.add_data(text)
    qr_creator.make(fit=True)
    img = qr_creator.make_image(fill_color=fill_color, back_color=back_color)

    img.save(output_path)
    return output_path

if __name__ == "__main__":
    generate_qr(text="yea boiiiiiiiiii", output_file_name="demo.png")
