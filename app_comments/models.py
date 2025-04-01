from django.db import models
from app_struct.models import *
# from app_econ.models import Project

class Comment(models.Model):
    name = models.TextField(blank=False, null=False, help_text="Краткие сведения", verbose_name="Краткие сведения")
    full_name = models.TextField(blank=False, null=False, help_text="Полный комментарий", verbose_name="Полный комментарий")
    created = models.DateTimeField(auto_now=True, help_text="Дата создания", verbose_name="Дата создания")
    actual = models.BooleanField(default=True, help_text="Актуальность", verbose_name="Актуальность")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, help_text="Компания", verbose_name="Компания")
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True, help_text="Подразделение", verbose_name="Подразделение")
    project = models.ForeignKey('app_econ.Project', on_delete=models.SET_NULL, blank=True, null=True, help_text="Проект", verbose_name="Проект")
    license = models.ForeignKey(License, on_delete=models.SET_NULL, blank=True, null=True, help_text="Лицензионный участок", verbose_name="Лицензионный участок")
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, blank=True, null=True, help_text="Объект", verbose_name="Объект")
    files_id = models.TextField(blank=True, null=True, help_text="ID файлов", verbose_name="ID файлов")
    user_created = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, help_text="Сотрудник", verbose_name="Сотрудник")
    documents = models.ManyToManyField('app_doc.Document', blank=True, related_name="comments", help_text="Документы, связанные с этим комментарием")


    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.name}'