from django.db import models

# Create your models here.

class Personnel_Item(models.Model):
    AFSN = models.CharField(max_length=200)
    RANK = models.CharField(max_length=200)
    FULLNAME = models.CharField(max_length=200)
    UNIT = models.CharField(max_length=200)

    def __str__(self):
        return self.FFULLNAME
    

class Placement(models.Model):
    FULLNAME = models.CharField(max_length=200)
    PresentUNIT = models.CharField(max_length=200)
    subUNIT = models.CharField(max_length=200)
    reassignedDATE = models.CharField(max_length=200)
    dateORDER = models.CharField(max_length=200)

    def __str__(self):
        return self.FULLNAME


    

