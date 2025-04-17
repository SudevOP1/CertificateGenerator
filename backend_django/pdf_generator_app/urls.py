from django.urls import path
from .views import *

urlpatterns = [
    path(
        "get-demo-certificate/",
        get_demo_certificate,
        name="get_demo_certificate"
    ),
    path(
        "send-emails/",
        send_emails,
        name="send_emails"
    ),
    path(
        "get-certificate/<int:id>",
        get_certificate,
        name="get_certificate"
    ),
]
