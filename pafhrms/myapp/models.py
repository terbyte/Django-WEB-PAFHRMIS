from django.db import models
from datetime import date


# New Define Tables -> Will be use in database
class tbl_Personnel(models.Model):
    PK_Personnel = models.BigAutoField(primary_key=True)
    FirstName = models.CharField(max_length=200)
    MiddleName = models.CharField(max_length=200, blank=True, null=True)
    LastName = models.CharField(max_length=200)
    NameSuffix = models.CharField(max_length=200, blank=True, null=True)
    AFPSN = models.CharField(max_length=200)
    Rank = models.CharField(max_length=200)
    BOS = models.CharField(max_length=200)
    Sex = models.CharField(max_length=10)
    Birthday = models.DateField(blank=True, null=True)
    ContactNumber = models.CharField(max_length=200, blank=True, null=True)
    EmailAddress = models.CharField(max_length=200, blank=True, null=True)
    Address = models.CharField(max_length=200, blank=True, null=True)
    Classification = models.CharField(max_length=200, blank=True, null=True)
    PersCategory = models.CharField(max_length=200, blank=True, null=True)
    SourceOfCommissionEnlistment = models.CharField(max_length=200, blank=True, null=True)
    PilotRated_NonRated = models.CharField(max_length=200, blank=True, null=True)
    AFSC_PRIMARY = models.CharField(max_length=200, blank=True, null=True)
    AFSC_SECONDARY = models.CharField(max_length=200, blank=True, null=True)
    AFSC_TERTIARY = models.CharField(max_length=200, blank=True, null=True)
    HighestPMEcourse = models.CharField(max_length=200, blank=True, null=True)
    EffectiveDateOfAppointment = models.DateField(blank=True, null=True)
    DateEnteredMilitary = models.DateField()
    DateLastPromotionAppointment = models.DateField(blank=True, null=True)
    Unit = models.CharField(max_length=200, blank=True, null=True)
    SubUnit = models.CharField(max_length=200, blank=True, null=True)
    DateUnitAssigned = models.DateField(blank=True, null=True)
    DateLastFullReenlistment = models.DateField(blank=True, null=True)
    DateLastETAD = models.DateField(blank=True, null=True)
    BachelorsDegree = models.CharField(max_length=200, blank=True, null=True)
    HighestAttainment = models.CharField(max_length=200, blank=True, null=True)
    SchoolAttended = models.CharField(max_length=200, blank=True, null=True)
    WithEligibility = models.CharField(max_length=200, blank=True, null=True)
    EligibilityDescription = models.CharField(max_length=200, blank=True, null=True)
    isActive = models.BooleanField(default=True)

class PersonnelFile(models.Model):
    personnel = models.ForeignKey(tbl_Personnel, related_name='files', on_delete=models.CASCADE)
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
    

class tbl_PersonnelPlacement(models.Model):
    PK_PersonnelPlacement = models.BigAutoField(primary_key=True)
    FK_Personnel = models.ForeignKey(tbl_Personnel, on_delete=models.CASCADE)
    FK_Unit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE, related_name='assignments')
    AssignmentCategory = models.CharField(max_length=200)
    DateFiled = models.DateField()
    MotherUnit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE, related_name='mother_unit_placements')
    AssigningUnit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE, related_name='assigning_unit_placements')
    Subunit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE, related_name='subunit_placements', null=True, blank=True)
    EffectiveDate = models.DateField()
    EffectiveUntil = models.DateField()
    Duration = models.CharField(max_length=200)
    IsArchived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.FK_Personnel} - {self.FK_Unit}"
    
# this is the old one / as of now, it is still using the old placement
class tbl_PersonnelFiles(models.Model):
    PK_PersonnelPlacement = models.ForeignKey(tbl_PersonnelPlacement, related_name='files', on_delete=models.CASCADE)
    Files = models.FileField(upload_to="orders/")
    UploadedOn = models.DateTimeField(auto_now_add=True)
    FK_Personnel = models.ForeignKey(tbl_Personnel, on_delete=models.CASCADE)






# class tbl_AFSCTable(models.Model):
#     PK_AFSC = models.BigAutoField(primary_key=True)
#     AFSCTitle = models.CharField(max_length=100)
#     AFSCDescription = models.CharField(max_length=200)

# class tbl_CoursesTable(models.Model):
#     PK_Course = models.BigAutoField(primary_key=True)
#     CourseTitle = models.CharField(max_length=200)
#     CourseDescription = models.CharField(max_length=200)
#     RelatedCourse = models.CharField(max_length=200)
    
# class tbl_AFSCCourseTable(models.Model):
#     PK_AFSCCourse = models.BigAutoField(primary_key=True)
#     RelatedCourse = models.CharField(max_length=100)
#     FK_AFSC= models.ForeignKey(AFSCTable, on_delete=models.CASCADE)
#     FK_Course = models.ForeignKey(CoursesTable, on_delete=models.CASCADE)

# class tbl_AFSCRelatedCourse(models.Model):
#     PK_AFSCRelatedCourse = models.BigAutoField(primary_key=True)
#     UnitName = models.CharField(max_length=100)
#     UnitDescription = models.CharField(max_length=200)
#     Logo = models.CharField(max_length=100)
#     FK_MotherUnit = models.ForeignKey('self', on_delete=models.CASCADE)

# class tbl_PersonnelHistoryTable(models.Model):
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



# class tbl_PositionTypeTable(models.Model):
#     PK_PositionType = models.BigAutoField(primary_key=True)
#     TypeTitle = models.CharField(max_length=100)
#     TypeDescription = models.CharField(max_length=100)

# class tbl_UnitWorkPositionTable(models.Model):
#     PK_UnitWorkPosition = models.BigAutoField(primary_key=True)
#     PositionTitle = models.CharField(max_length=100)
#     PositionDescription = models.CharField(max_length=100)
#     FK_PositionType = models.ForeignKey(PositionTypeTable, on_delete=models.CASCADE)
#     FK_Unit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE)
    
# class tbl_PositionSuggestedAFSC(models.Model):
#     PK_UnitWorkPosition = models.BigAutoField(primary_key=True)
#     PositionTitle = models.CharField(max_length=100)
#     PositionDescription = models.CharField(max_length=100)
#     FK_PositionType = models.ForeignKey(PositionTypeTable, on_delete=models.CASCADE)
#     FK_Unit = models.ForeignKey(UnitsTable, on_delete=models.CASCADE)