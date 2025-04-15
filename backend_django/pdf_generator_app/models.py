from django.db import models

# Create your models here.

class Entry(models.Model):
    organizer_name = models.CharField(max_length=50)
    workshop_name  = models.CharField(max_length=50)
    date           = models.DateField()

class Attendee(models.Model):
    entry_id = models.ForeignKey(Entry, on_delete=models.CASCADE)
    name    = models.CharField(max_length=50)
    email   = models.EmailField()
