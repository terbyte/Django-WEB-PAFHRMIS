# Generated by Django 5.0.6 on 2024-05-14 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_personnel_item_date_entered_personnel_item_nr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel_item',
            name='AFSC',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='personnel_item',
            name='AFSN',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='personnel_item',
            name='CONTACT_NUMBER',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='personnel_item',
            name='SERIAL_NUMBER',
            field=models.CharField(max_length=200),
        ),
    ]
