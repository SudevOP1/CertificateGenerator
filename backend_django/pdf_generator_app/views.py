from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .pdf_generator.generator import get_pdf_file
from .qr_generator.generator import generate_qr

demo_qr_path = "file:///C:/Users/Sudev/Desktop/Sudev D/DJ/Python/Python Mini Project/backend_django/pdf_generator_app/pdf_generator/demo_qr.png"

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
            

            # generate QR imgs
            # generate pdfs using QRs
            # send emails
            # if error, remove data from database

            return JsonResponse({"message": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"message": "something went wrong", "error": str(e)}, status=400)
    return JsonResponse({"message": "Only POST requests allowed"}, status=405)

#TODO
def get_certificate(request):
    return JsonResponse({"message": "To be done"})
