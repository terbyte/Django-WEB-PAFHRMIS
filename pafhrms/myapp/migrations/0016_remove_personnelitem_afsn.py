# Generated by Django 5.0.6 on 2024-05-14 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_personnelitem_afsn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personnelitem',
            name='AFSN',
        ),
    ]