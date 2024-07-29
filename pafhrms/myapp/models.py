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


class PersonnelFile(models.Model):
    personnel = models.ForeignKey(PersonnelItem, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='personnel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return f'{self.RANK} {self.LAST_NAME}, {self.FIRST_NAME} {self.MIDDLE_NAME} {self.EXTENSION_NAME}'
    

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
    ORDER_UPLOADFILE = models.FileField(upload_to='orders/')
    IS_ARCHIVED = models.BooleanField(default=False)

    class Meta:
        db_table = "placementinfo"


class UnitsTable(models.Model):
    PK_Units = models.BigAutoField (primary_key=True)
    UnitName = models.CharField(max_length=100)
    UnitDescription = models.CharField(max_length=200)
    UnitCategory = models.CharField(max_length=200)
    Logo = models.CharField(max_length=200, blank=True, null=True)
    FK_MotherUnit = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.UnitName
    

# # New Define Tables -> Will be use in database
# class PersonnelTable(models.Model):
#     PK_Personnel = models.BigAutoField(primary_key=True)
#     FirstName = models.CharField(max_length=200)
#     LastName = models.CharField(max_length=200)    
#     MiddleName = models.CharField(max_length=200, blank=True, null=True)
#     NameSuffix = models.CharField(max_length=200, blank=True, null=True)
#     BOS = models.CharField(max_length=200)
#     Sex = models.CharField(max_length=10)
#     Birthday = models.DateField(blank=True, null=True)
#     ContactNumber = models.CharField(max_length=200, blank=True, null=True)
#     Address = models.CharField(max_length=200, blank=True, null=True)
#     SerialNumber = models.CharField(max_length=200)
#     Rank = models.CharField(max_length=200)
#     DateEnlisted = models.DateField(blank=True, null=True)
#     DatePromoted = models.DateField(blank=True, null=True)
#     TypeOfPersonnel = models.DateField(blank=True)
#     isActive = models.BooleanField(default=True)

# class AFSCTable(models.Model):
#     PK_AFSC = models.BigAutoField(primary_key=True)
#     AFSCTitle = models.CharField(max_length=100)
#     AFSCDescription = models.CharField(max_length=200)

# class CoursesTable(models.Model):
#     PK_Course = models.BigAutoField(primary_key=True)
#     CourseTitle = models.CharField(max_length=200)
#     CourseDescription = models.CharField(max_length=200)
#     RelatedCourse = models.CharField(max_length=200)
    
# class AFSCCourseTable(models.Model):
#     PK_AFSCCourse = models.BigAutoField(primary_key=True)
#     RelatedCourse = models.CharField(max_length=100)
#     FK_AFSC= models.ForeignKey(AFSCTable, on_delete=models.CASCADE)
#     FK_Course = models.ForeignKey(CoursesTable, on_delete=models.CASCADE)

# class AFSCRelatedCourse(models.Model):
#     PK_AFSCRelatedCourse = models.BigAutoField(primary_key=True)
#     UnitName = models.CharField(max_length=100)
#     UnitDescription = models.CharField(max_length=200)
#     Logo = models.CharField(max_length=100)
#     FK_MotherUnit = models.ForeignKey('self', on_delete=models.CASCADE)

# class PersonnelHistoryTable(models.Model):
#     PK_Personnel = models.BigAutoField(primary_key=True)
#     FirstName = models.CharField(max_length=100)
#     LastName = models.CharField(max_length=100)    
#     MiddleName = models.CharField(max_length=100, blank=True)
#     NameSuffix = models.CharField(max_length=50, blank=True)
#     BOS = models.CharField(max_length=100)
#     Sex = models.CharField(max_length=10)
#     Birthday = models.DateField(blank=True)
#     ContactNumber = models.CharField(max_length=200, blank=True)
#     Address = models.CharField(max_length=200, blank=True)
#     SerialNumber = models.CharField(max_length=200)
#     Rank = models.CharField(max_length=200)
#     DateEnlisted = models.DateField(blank=True)
#     DatePromoted = models.DateField(blank=True, null=True)
#     TypeOfPersonnel = models.DateField(blank=True)
#     DateEdited = models.DateField(default=date.today)
#     FK_Personnel = models.ForeignKey(PersonnelTable, on_delete=models.CASCADE)

# class PersonnelFilesTable(models.Model):
#     PK_PersonnelFiles = models.BigAutoField(primary_key=True)
#     DateUploaded = models.DateField(default=date.today)
#     FileName = models.CharField(max_length=200)
#     FileType = models.CharField(max_length=200)
#     FileLocation= models.CharField(max_length=200)
#     FK_Personnel = models.ForeignKey(PersonnelTable, on_delete=models.CASCADE)

# class PositionTypeTable(models.Model):
#     PK_PositionType = models.BigAutoField(primary_key=True)
#     TypeTitle = models.CharField(max_length=100)
#     TypeDescription = models.CharField(max_length=100)

# class UnitWorkPositionTable(models.Model):
#     PK_UnitWorkPosition = models.BigAutoField(primary_key=True)
#     PositionTitle = models.CharField(max_length=100)
#     PositionDescription = models.CharField(max_length=100)
#     FK_PositionType = models.ForeignKey(PositionTypeTable, on_delete=models.CASCADE)
#     FK_Unit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE)
    
# class PositionSuggestedAFSC(models.Model):
#     PK_UnitWorkPosition = models.BigAutoField(primary_key=True)
#     PositionTitle = models.CharField(max_length=100)
#     PositionDescription = models.CharField(max_length=100)
#     FK_PositionType = models.ForeignKey(PositionTypeTable, on_delete=models.CASCADE)
#     FK_Unit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE)