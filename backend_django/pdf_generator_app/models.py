from django.db import models

# Create your models here.

class Workshop(models.Model):
    organizer_name  = models.CharField(max_length=50)
    workshop_name   = models.CharField(max_length=50)
    date            = models.DateField()
    emails_sent     = models.BooleanField(default=False)

class Attendee(models.Model):
    workshop_id = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    name        = models.CharField(max_length=50)
    email       = models.EmailField()
