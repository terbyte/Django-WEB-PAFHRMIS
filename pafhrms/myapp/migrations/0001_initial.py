# Generated by Django 5.0.6 on 2024-08-08 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Placement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AFPSN', models.CharField(max_length=200)),
                ('RANK', models.CharField(max_length=200)),
                ('LAST_NAME', models.CharField(max_length=200)),
                ('FIRST_NAME', models.CharField(max_length=200)),
                ('MIDDLE_NAME', models.CharField(max_length=200)),
                ('SUFFIX', models.CharField(max_length=200)),
                ('MOTHER_UNIT', models.CharField(max_length=200)),
                ('NEW_UNIT', models.CharField(max_length=200)),
                ('SUB_UNIT', models.CharField(blank=True, max_length=200, null=True)),
                ('REASSIGN_EFFECTIVEDDATE', models.DateField()),
                ('ASSIGNMENT_CATEGORY', models.CharField(max_length=200)),
                ('DURATION', models.CharField(blank=True, max_length=200, null=True)),
                ('REASSIGN_EFFECTIVEDDATE_UNTIL', models.DateField(blank=True, null=True)),
                ('ORDER_UPLOADFILE', models.FileField(upload_to='orders/')),
                ('IS_ARCHIVED', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'placementinfo',
            },
        ),
        migrations.CreateModel(
            name='tbl_AFSC',
            fields=[
                ('PK_AFSC', models.BigAutoField(primary_key=True, serialize=False)),
                ('AFSCCode', models.CharField(max_length=100)),
                ('AFSCDescription', models.CharField(max_length=200)),
                ('AFSCLevel', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='tbl_Personnel',
            fields=[
                ('PK_Personnel', models.BigAutoField(primary_key=True, serialize=False)),
                ('FirstName', models.CharField(max_length=200)),
                ('MiddleName', models.CharField(blank=True, max_length=200, null=True)),
                ('LastName', models.CharField(max_length=200)),
                ('NameSuffix', models.CharField(blank=True, max_length=200, null=True)),
                ('AFPSN', models.CharField(max_length=200)),
                ('Rank', models.CharField(max_length=200)),
                ('BOS', models.CharField(max_length=200)),
                ('Sex', models.CharField(max_length=10)),
                ('Birthday', models.DateField(blank=True, null=True)),
                ('ContactNumber', models.CharField(blank=True, max_length=200, null=True)),
                ('EmailAddress', models.CharField(blank=True, max_length=200, null=True)),
                ('Address', models.CharField(blank=True, max_length=200, null=True)),
                ('Classification', models.CharField(blank=True, max_length=200, null=True)),
                ('PersCategory', models.CharField(blank=True, max_length=200, null=True)),
                ('SourceOfCommissionEnlistment', models.CharField(blank=True, max_length=200, null=True)),
                ('PilotRated_NonRated', models.CharField(blank=True, max_length=200, null=True)),
                ('AFSC_PRIMARY', models.CharField(blank=True, max_length=200, null=True)),
                ('AFSC_SECONDARY', models.CharField(blank=True, max_length=200, null=True)),
                ('AFSC_TERTIARY', models.CharField(blank=True, max_length=200, null=True)),
                ('HighestPMEcourse', models.CharField(blank=True, max_length=200, null=True)),
                ('EffectiveDateOfAppointment', models.DateField(blank=True, null=True)),
                ('DateEnteredMilitary', models.DateField()),
                ('DateLastPromotionAppointment', models.DateField(blank=True, null=True)),
                ('Unit', models.CharField(blank=True, max_length=200, null=True)),
                ('SubUnit', models.CharField(blank=True, max_length=200, null=True)),
                ('DateUnitAssigned', models.DateField(blank=True, null=True)),
                ('DateLastFullReenlistment', models.DateField(blank=True, null=True)),
                ('DateLastETAD', models.DateField(blank=True, null=True)),
                ('BachelorsDegree', models.CharField(blank=True, max_length=200, null=True)),
                ('HighestAttainment', models.CharField(blank=True, max_length=200, null=True)),
                ('SchoolAttended', models.CharField(blank=True, max_length=200, null=True)),
                ('WithEligibility', models.CharField(blank=True, max_length=200, null=True)),
                ('EligibilityDescription', models.CharField(blank=True, max_length=200, null=True)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonnelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='personnel_files/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='myapp.tbl_personnel')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_PersonnelPlacement',
            fields=[
                ('PK_PersonnelPlacement', models.BigAutoField(primary_key=True, serialize=False)),
                ('AssignmentCategory', models.CharField(max_length=200)),
                ('DateFiled', models.DateField()),
                ('EffectiveDate', models.DateField()),
                ('EffectiveUntil', models.DateField()),
                ('Duration', models.CharField(max_length=200)),
                ('IsArchived', models.BooleanField(default=False)),
                ('FK_Personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tbl_personnel')),
            ],
        ),
        migrations.CreateModel(
            name='tbl_PersonnelFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Files', models.FileField(upload_to='orders/')),
                ('UploadedOn', models.DateTimeField(auto_now_add=True)),
                ('FK_Personnel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tbl_personnel')),
                ('PK_PersonnelPlacement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='myapp.tbl_personnelplacement')),
            ],
        ),
        migrations.CreateModel(
            name='UnitsTable',
            fields=[
                ('PK_Units', models.BigAutoField(primary_key=True, serialize=False)),
                ('UnitName', models.CharField(max_length=100)),
                ('UnitDescription', models.CharField(max_length=200)),
                ('UnitCategory', models.CharField(max_length=200)),
                ('Logo', models.CharField(blank=True, max_length=200, null=True)),
                ('FK_MotherUnit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.unitstable')),
            ],
        ),
        migrations.AddField(
            model_name='tbl_personnelplacement',
            name='AssigningUnit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigning_unit_placements', to='myapp.unitstable'),
        ),
        migrations.AddField(
            model_name='tbl_personnelplacement',
            name='FK_Unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='myapp.unitstable'),
        ),
        migrations.AddField(
            model_name='tbl_personnelplacement',
            name='MotherUnit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mother_unit_placements', to='myapp.unitstable'),
        ),
        migrations.AddField(
            model_name='tbl_personnelplacement',
            name='Subunit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subunit_placements', to='myapp.unitstable'),
        ),
    ]
