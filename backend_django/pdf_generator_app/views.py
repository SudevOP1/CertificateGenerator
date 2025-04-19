from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, os, smtplib, base64
from .pdf_generator.generator import get_pdf_file
from .qr_generator.generator import generate_qr
from .models import *
from email.message import EmailMessage

demo_qr_path = f"file:///C{os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")[1:]}/pdf_generator/demo_qr.png"
website_url = "http://127.0.0.1:8000"


@csrf_exempt
def get_demo_certificate(request):
    """
    POST body = {
        "organizer_name": "Sudev Dahitule111",
        "workshop_name": "Python in 69 Hours111",
        "date": "yyyy-dd-mm",
        "attendees": [
            {"name": "Sahad Mithani", "email": "sahadmithani@gmail.com"},
            {"name": "Smit Doshi", "email": "smitdoshi205@gmail.com"}
        ]
    }
    """
    if request.method == "POST":
        try:
            body_data = json.loads(request.body)
            organizer_name = body_data["organizer_name"]
            workshop_name = body_data["workshop_name"]
            date = body_data["date"]
            attendees = body_data["attendees"]
            attendee = attendees[0]

            pdf_base64 = get_pdf_file(
                organizer_name=organizer_name,
                workshop_name=workshop_name,
                date=date,
                qr=demo_qr_path,
                attendee_name=attendee["name"],
                attendee_email=attendee["email"]
            )

            return JsonResponse({
                "message": "success",
                "certificate": pdf_base64,
                "type": "base64-pdf"
            }, status=200)

        except Exception as e:
            return JsonResponse({"message": "something went wrong", "error": str(e)}, status=400)
    return JsonResponse({"message": "Only POST requests allowed"}, status=405)

@csrf_exempt
def send_emails(request):
    """
    POST body = {
        "organizer_name": "Sudev Dahitule111",
        "workshop_name": "Python in 69 Hours111",
        "date": "yyyy-dd-mm",
        "attendees": [
            {"name": "Sahad Mithani", "email": "sahadmithani@gmail.com"},
            {"name": "Smit Doshi", "email": "smitdoshi205@gmail.com"}
        ],
        "sender_email": "sudevdahitule06@gmail.com",
        "sender_email_password": "abcd abcd abcd abcd",
        "email_subject": "Python in 69 Hours Workshop Certificate111",
        "email_body": "Thank you very much for attending our workshop.\nPlease find the certificate attached.\nThank You111"
    }
    """
    if request.method == "POST":
        try:
            # extract data from body
            body_data = json.loads(request.body)
            organizer_name = body_data["organizer_name"]
            workshop_name = body_data["workshop_name"]
            date = body_data["date"]
            sender_email = body_data["sender_email"]
            sender_email_password = body_data["sender_email_password"]
            email_subject = body_data["email_subject"]
            email_body = body_data["email_body"]
            attendees = body_data["attendees"]

            # save data in database
            new_workshop_obj = Workshop.objects.create(
                organizer_name  = organizer_name,
                organizer_email = sender_email,
                workshop_name   = workshop_name,
                date            = date,
                emails_sent     = False,
            )
            new_attendee_objs = [
                Attendee(
                    workshop_id = new_workshop_obj,
                    name        = attendee["name"],
                    email       = attendee["email"],
                ) for attendee in attendees
            ]
            Attendee.objects.bulk_create(new_attendee_objs)

            # generate QR imgs and save paths
            qr_paths = {}
            for attendee_obj in new_attendee_objs:
                certificate_url = website_url + f"/certificate/{attendee_obj.id}"
                qr_filename = f"output_{attendee_obj.id}.png"
                qr_output_path = generate_qr(text=certificate_url, output_file_name=qr_filename)
                qr_paths[attendee_obj.id] = qr_output_path

            # generate pdfs using saved QR paths
            base64_encoded_pdfs = {}
            for attendee_obj in new_attendee_objs:
                qr_output_path = qr_paths[attendee_obj.id]
                qr_uri_path = f"file:///{qr_output_path.replace(os.sep, '/')}"

                pdf_base64 = get_pdf_file(
                    organizer_name = new_workshop_obj.organizer_name,
                    workshop_name  = new_workshop_obj.workshop_name,
                    date           = str(new_workshop_obj.date),
                    qr             = qr_uri_path,
                    attendee_name  = attendee_obj.name,
                    attendee_email = attendee_obj.email,
                )
                base64_encoded_pdfs[attendee_obj.id] = pdf_base64

            # send emails
            for attendee_obj in new_attendee_objs:
                pdf_base64 = base64_encoded_pdfs[attendee_obj.id]
                pdf_bytes = base64.b64decode(pdf_base64)

                msg = EmailMessage()
                msg['Subject'] = email_subject
                msg['From'] = sender_email
                msg['To'] = attendee_obj.email
                msg.set_content(email_body)

                # Add attachment
                msg.add_attachment(
                    pdf_bytes,
                    maintype='application',
                    subtype='pdf',
                    filename=f"{attendee_obj.name}_certificate.pdf"
                )

                # Send email using Gmail SMTP
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(sender_email, sender_email_password)
                    smtp.send_message(msg)
            new_workshop_obj.emails_sent = True

            return JsonResponse({"message": "success"}, status=200)
        
        # if error, remove data from database
        except Exception as e:
            if 'new_workshop_obj' in locals():
                new_workshop_obj.delete()
            return JsonResponse({"message": "something went wrong", "error": str(e)}, status=400)
        
        # delete QR imgs
        finally:
            if "qr_paths" in locals():
                for path in qr_paths.values():
                    if os.path.exists(path):
                        os.remove(path)
        
    return JsonResponse({"message": "Only POST requests allowed"}, status=405)

@csrf_exempt
def get_certificate(request):
    """
    POST body = {
        "attendee_id": "24"
    }
    """
    if request.method == "POST":
        try:
            # extract attendee_id from body
            attendee_id = json.loads(request.body)["attendee_id"]
            attendee_obj = Attendee.objects.get(id=attendee_id)
            workshop_obj = attendee_obj.workshop_id

            # generate QR img and save path
            certificate_url = website_url + f"/certificate/{attendee_id}"
            qr_filename = f"output_{attendee_id}.png"
            qr_output_path = generate_qr(text=certificate_url, output_file_name=qr_filename)
            
            # generate pdf using saved QR path
            qr_uri_path = f"file:///{qr_output_path.replace(os.sep, '/')}"
            pdf_base64 = get_pdf_file(
                organizer_name = workshop_obj.organizer_name,
                workshop_name  = workshop_obj.workshop_name,
                date           = str(workshop_obj.date),
                qr             = qr_uri_path,
                attendee_name  = attendee_obj.name,
                attendee_email = attendee_obj.email,
            )
            return JsonResponse({
                "message": "success",
                "certificate": pdf_base64,
                "type": "base64-pdf"
            }, status=200)
        
        except Exception as e:
            return JsonResponse({"message": "something went wrong", "error": str(e)}, status=400)
        
        # delete QR img
        finally:
            if "qr_output_path" in locals() and os.path.exists(qr_output_path):
                os.remove(qr_output_path)
        
    return JsonResponse({"message": "Only POST requests allowed"}, status=405)
