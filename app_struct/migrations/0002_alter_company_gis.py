# Generated by Django 5.1.4 on 2025-01-27 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_struct', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='gis',
            field=models.CharField(blank=True, help_text='GIS ID', max_length=255, null=True, verbose_name='GIS ID'),
        ),
    ]
