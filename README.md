# Certificate Generator

This is my Semester 4 Python mini project".<br>
It is a Django-based web application that generates personalized digital certificates for event participants.<br>
The app takes user input, adds details to a certificate template, and emails the certificate to recipients.<br>
It also includes a QR code for verification.<br>
<br>

## 💡 What it does
- Input participant details<br>
  → Manually or<br>
  → Upload Excel file with multiple entries
- Automatically generate certificates using a template
- Each certificate includes a unique QR code for verification
- Send the certificates to participant emails instantly
- Scan the QR code to view and verify the certificate online
<br>

## 🛠️ Tech Stacks
- **Frontend**: `Html`, `CSS`, `Javascript`
- **Backend**: `Django`
- **Libraries Used**: `jinja2`, `pdfkit`, `qrcode`
<br>

## ✨ Website Design
![Example](https://raw.githubusercontent.com/SudevOP1/CertificateGenerator/main/Implementation.png)<br>
<br>

## 🚀 How to run it locally

### 1. Clone the repo
```bash
git clone https://github.com/SudevOP1/CertificateGenerator.git
```
### 2. Install wkhtmltopdf
Visit `https://wkhtmltopdf.org/downloads.html` and install latest stable version for your device.
### 3. Backend Server
```powershell
cd CertificateGenerator/backend
pip install -r requirements.txt
python manage.py makemigratiosn
python manage.py migrate
python manage.py runserver
```
### 4. Frontend Server
```powershell
cd CertificateGenerator/frontend
code .
```
Use the `Live Server` extnesion to run `input.html`
### 5. See the magic happen
Open `http://127.0.0.1:5500/input.html` in your browser<br>
