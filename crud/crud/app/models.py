from django.db import models

# Create your models here.


class RecordTable(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=50, default='Islamabad')

