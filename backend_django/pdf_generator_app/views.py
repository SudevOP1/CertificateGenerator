from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, os
from .pdf_generator.generator import get_pdf_file
from .qr_generator.generator import generate_qr
from .models import *

demo_qr_path = "file:///C:/Users/Sudev/Desktop/Sudev D/DJ/Python/Python Mini Project/backend_django/pdf_generator_app/pdf_generator/demo_qr.png"
website_url = "http://127.0.0.1:8000"

@csrf_exempt
def get_demo_certificate(request):
    """
    POST body = {
        "organizer_name": "Smit Doshi",
        "workshop_name": "Python in 69 Hours",
        "date": "dd-mm-yyyy",
        "attendees": [
            {"name": "Sahad Mithani", "email": "sahadmithani@gmail.com"},
            {"name": "Sudev Dahitule", "email": "sudevdahitule@gmail.com"}
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

# TODO
@csrf_exempt
def send_emails(request):
    """
    POST body = {
        "organizer_name": "Smit Doshi",
        "workshop_name": "Python in 69 Hours",
        "date": "dd-mm-yyyy",
        "attendees": [
            {"name": "Sahad Mithani", "email": "sahadmithani@gmail.com"},
            {"name": "Sudev Dahitule", "email": "sudevdahitule@gmail.com"}
        ]
    }
    """
    if request.method == "POST":
        try:
            # extract data from body
            body_data = json.loads(request.body)
            organizer_name = body_data["organizer_name"]
            workshop_name = body_data["workshop_name"]
            date = body_data["date"]
            attendees = body_data["attendees"]

            # save data in database
            new_workshop_obj = Workshop.objects.create(
                organizer_name  = organizer_name,
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

            # send emails TODO From Here
            # delete QR imgs
            # if error, remove data from database

            return JsonResponse({"message": "success", "pdfs": base64_encoded_pdfs}, status=200)
        except Exception as e:
            return JsonResponse({"message": "something went wrong", "error": str(e)}, status=400)
    return JsonResponse({"message": "Only POST requests allowed"}, status=405)

#TODO
def get_certificate(request):
    return JsonResponse({"message": "To be done"})
