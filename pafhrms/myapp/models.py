from django.db import models

# Create your models here.

class Personnel_Item(models.Model):
    _NR = models.CharField(max_length=200)
    _AFSN = models.CharField(max_length=200)
    _RANK = models.CharField(max_length=200)
    _FULLNAME = models.CharField(max_length=200)
    _UNIT = models.CharField(max_length=200)

    def __str__(self):
        return self._FULLNAME