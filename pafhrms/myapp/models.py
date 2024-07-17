from django.db import models

class PersonnelItem(models.Model):
    RANK = models.CharField(max_length=200)
    LAST_NAME = models.CharField(max_length=200)
    FIRST_NAME = models.CharField(max_length=200)
    MIDDLE_NAME = models.CharField(max_length=200, blank=True, null=True)
    EXTENSION_NAME = models.CharField(max_length=200, blank=True, null=True)
    SERIAL_NUMBER = models.CharField(max_length=200)
    BOS = models.CharField(max_length=200)
    SEX = models.CharField(max_length=10)
    BIRTHDAY = models.DateField(blank=True, null=True)
    CONTACT_NUMBER = models.CharField(max_length=200, blank=True, null=True)
    ADDRESS = models.CharField(max_length=200, blank=True, null=True)
    CLASSIFICATION = models.CharField(max_length=200)
    CATEGORY = models.CharField(max_length=200)
    SOURCE_OF_ENLISTMENT_COMMISION = models.CharField(max_length=200)
    PILOT_RATED_NON_RATED = models.CharField(max_length=200, blank=True, null=True)
    AFSC = models.CharField(max_length=200, blank=True, null=True)
    HIGHEST_PME_COURSES = models.CharField(max_length=200, blank=True, null=True)
    EFFECTIVE_DATE_APPOINTMENT = models.DateField()
    EFFECTIVE_DATE_ENTERED = models.DateField()
    DATE_LAST_PROMOTION_APPOINTMENT = models.DateField(blank=True, null=True)
    UNIT = models.CharField(max_length=200, blank=True, null=True)
    SUB_UNIT = models.CharField(max_length=200, blank=True, null=True)
    DATE_LASTFULL_REENLISTMENT = models.DateField(blank=True, null=True)
    DATE_LAST_ETAD = models.DateField(blank=True, null=True)
    INACTIVITY_REASON=models.CharField(max_length=200, blank=True, null=True)
    IS_ACTIVE = models.BooleanField(default=True)


class Placement(models.Model):
    AFPSN = models.CharField(max_length=200)
    RANK = models.CharField(max_length=200)
    LAST_NAME = models.CharField(max_length=200)
    FIRST_NAME = models.CharField(max_length=200)
    MIDDLE_NAME = models.CharField(max_length=200)
    SUFFIX = models.CharField(max_length=200)
    MOTHER_UNIT = models.CharField(max_length=200)
    NEW_UNIT = models.CharField(max_length=200)
    SUB_UNIT = models.CharField(max_length=200, blank=True, null=True)
    REASSIGN_EFFECTIVEDDATE = models.DateField()
    ASSIGNMENT_CATEGORY = models.CharField(max_length=200)
    DURATION = models.CharField(max_length=200, blank=True, null=True)
    REASSIGN_EFFECTIVEDDATE_UNTIL = models.DateField(blank=True, null=True)
    IS_ARCHIVED = models.BooleanField(default=False)

    class Meta:
        db_table = "placementinfo"


class PersonnelFile(models.Model):
    placement = models.ForeignKey(Placement, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='orders/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    


# class AFSC(models.Model):
#     code = models.CharField(max_length=20, unique=True)
#     description = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.code

