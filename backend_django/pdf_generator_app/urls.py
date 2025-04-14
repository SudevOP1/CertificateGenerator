from django.urls import path
from .views import *

urlpatterns = [
    path("hello/", hello_world, name="hello_world"),
]
