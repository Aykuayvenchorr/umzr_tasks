from django.db import models

# Create your models here.

# Модель предприятия
class Company(models.Model):
    name        = models.CharField(max_length=250, unique=True, help_text="Наименование", verbose_name="Наименование")
    full_name   = models.CharField(max_length=250, help_text="Полное наименование", verbose_name="Полное наименование")
    parent      = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True, related_name="subcompany", help_text="Головная компания", verbose_name="Головная компания")
    logo        = models.ImageField(blank=True, null=True, upload_to="struct/company/logo/", help_text="Логотип", verbose_name="Логотип")
    contacts    = models.TextField(blank=True, null=True, help_text="Контакты", verbose_name="Контакты")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуальна", verbose_name="Актуальна")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    gis         = models.TextField(blank=True, null=True, help_text="GIS ID", verbose_name="GIS ID")

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ["name"]
        indexes = [models.Index(fields=['name']), ]
        # Уникальные вместе
        # unique_together = ['field1', 'field2']

    def __str__(self):
        return self.name