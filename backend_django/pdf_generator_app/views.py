from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
from pdf_generator.generator import get_pdf_file

def get_demo_qr(): return Image.open("./pdf_generator/demo_qr.png")

def get_qr():       return "yo" # TODO

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
                qr="demo_qr.png",
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

def send_emails(request): # TODO
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            # Process the data (just an example response)
            response_data = {
                "received": data,
                "message": "POST request received successfully",
                "status": "success"
            }
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=400)

    return JsonResponse({"message": "Only POST requests are allowed"}, status=405)
