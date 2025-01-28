# Generated by Django 5.1.4 on 2025-01-28 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_struct', '0006_license_actual'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Наименование', max_length=255, verbose_name='Наименование')),
                ('count', models.FloatField(blank=True, help_text='Количество', null=True, verbose_name='Количество')),
                ('length', models.FloatField(blank=True, help_text='Протяженность', null=True, verbose_name='Протяженность')),
                ('square', models.FloatField(blank=True, help_text='Площадь', null=True, verbose_name='Площадь')),
                ('note', models.TextField(blank=True, help_text='Примечание', null=True, verbose_name='Примечание')),
                ('actual', models.BooleanField(default=True, help_text='Актуально', verbose_name='Актуально')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Создан', verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Обновлен', verbose_name='Обновлен')),
                ('gis', models.CharField(blank=True, help_text='GIS ID', null=True, verbose_name='GIS ID')),
                ('gist', models.CharField(blank=True, help_text='Таблица в GIS', null=True, verbose_name='Таблица в GIS')),
                ('license', models.ManyToManyField(help_text='Лицензии', related_name='facilities', to='app_struct.license', verbose_name='Лицензии')),
                ('parent', models.ForeignKey(blank=True, help_text='Основной объект', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facilities', to='app_struct.facility', verbose_name='Основной объект')),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
                'indexes': [models.Index(fields=['name'], name='app_struct__name_08f878_idx')],
            },
        ),
    ]
