# Generated by Django 5.0.6 on 2024-05-14 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_rename_afsn_personnelitem_nr'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnelitem',
            name='AFSN',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
