from django.db import models
from django.contrib.auth.models import User

class Sities(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    NameSity = models.CharField(max_length=150)
    coordinate_lat = models.IntegerField()
    coordinate_lon = models.IntegerField()

    def __str__(self):
        return self.NameSity
    

