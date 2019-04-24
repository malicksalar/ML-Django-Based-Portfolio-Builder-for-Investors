from django.db import models

# Create your models here.


class form_data(models.Model):
    name = models.CharField(max_length=30)
    value = models.FloatField()
