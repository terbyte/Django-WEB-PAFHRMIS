from django.db import models

# Create your models here.

class Personnel_Item(models.Model):
    AFSN = models.CharField(max_length=200)
    _RANK = models.CharField(max_length=200)
    _FULLNAME = models.CharField(max_length=200)
    _UNIT = models.CharField(max_length=200)
