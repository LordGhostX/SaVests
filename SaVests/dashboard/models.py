from django.db import models
from datetime import datetime

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    active = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.email)
