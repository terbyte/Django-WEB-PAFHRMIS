from django.db import models

# Create your models here.

class PersonnelItem(models.Model):
    NR = models.CharField(max_length=200, blank=True, null=True)
    RANK = models.CharField(max_length=200)
    LAST_NAME = models.CharField(max_length=200)
    FIRST_NAME = models.CharField(max_length=200)
    MIDDLE_NAME = models.CharField(max_length=200)
    EXTENSION_NAME = models.CharField(max_length=200, blank=True, null=True)
    SERIAL_NUMBER = models.CharField(max_length=200)
    BOS = models.CharField(max_length=200)
    SEX = models.CharField(max_length=10)
    BIRTHDAY = models.DateField()
    CONTACT_NUMBER = models.CharField(max_length=200, blank=True, null=True)
    ADDRESS = models.CharField(max_length=200)
    REGULAR_RESERVE = models.CharField(max_length=200, blank=True, null=True)
    PILOT_RATED_NON_RATED = models.CharField(max_length=200, blank=True, null=True)
    AFSC = models.CharField(max_length=200, blank=True, null=True)
    HIGHEST_PME_COURSES = models.CharField(max_length=200, blank=True, null=True)
    EFFECTIVE_DATE_APPOINTMENT = models.DateField()
    EFFECTIVE_DATE_ENTERED = models.DateField()
    LENGTH_OF_SERVICE = models.CharField(max_length=200)
    DATE_LAST_PROMOTION_APPOINTMENT = models.DateField(max_length=200, blank=True, null=True)
    UNIT = models.CharField(max_length=200)
    SUB_UNIT = models.CharField(max_length=200, blank=True, null=True)
    DATE_LAST_1ST_TRANCH_REENLISTMENT = models.DateField(max_length=200, blank=True, null=True)
    DATE_LAST_2ND_TRANCH_REENLISTMENT = models.DateField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.RANK} {self.LAST_NAME}, {self.FIRST_NAME} {self.MIDDLE_NAME}'
    

# class PersonnelItem(models.Model):
#     RANK = models.CharField(max_length=200)
#     LAST_NAME = models.CharField(max_length=200)
#     FIRST_NAME = models.CharField(max_length=200)
#     MIDDLE_NAME = models.CharField(max_length=200)




class Placement(models.Model):
    FULLNAME = models.CharField(max_length=200)
    PresentUNIT = models.CharField(max_length=200)
    subUNIT = models.CharField(max_length=200)
    reassignedDATE = models.CharField(max_length=200)
    dateORDER = models.CharField(max_length=200)

    def __str__(self):
        return self.FULLNAME


    

