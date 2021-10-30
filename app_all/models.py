from django.db import models

# Create your models here

class Weather(models.Model):
    city = models.CharField(max_length=555)
    country = models.CharField(max_length=555)
    main = models.CharField(max_length=555)
    wind = models.FloatField()
    pressure = models.FloatField()
    humidity = models.FloatField()
    dt = models.CharField(max_length=50)