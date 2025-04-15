from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_demo_certificate(request):
    data = {
        'message': 'This is a GET request',
        'status': 'success'
    }
    return JsonResponse(data)

def send_emails(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            # Process the data (just an example response)
            response_data = {
                'received': data,
                'message': 'POST request received successfully',
                'status': 'success'
            }
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
