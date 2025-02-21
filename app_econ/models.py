import datetime
from django.utils import timezone
from django.db import models

from app_doc.models import Contract, Document
from app_struct.models import Company, Division, Employee, Facility, License
from django.core.validators import MinValueValidator


# Модель проекта
class ProjectActualManager(models.Manager):
    """Менеджер подразделений - только верхнеуровневые подразделения"""
    def get_queryset(self):
        return super().get_queryset().filter(actual=True)  
class Project(models.Model):
    """Проекты подразделения"""
    division    = models.ForeignKey(Division, on_delete=models.CASCADE, related_name="projects", help_text="Подразделение", verbose_name="Подразделение")
    name        = models.CharField(max_length=250, help_text="Наименование", verbose_name="Наименование")
    licenses    = models.ManyToManyField(License, related_name="projects", help_text="Лицензии", verbose_name="Лицензии")
    contacts    = models.TextField(blank=True, null=True, help_text="Контакты", verbose_name="Контакты")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['division', 'name']
        indexes = [models.Index(fields=['division', 'name']),]
        unique_together = ('division', 'name')
    
    objects = models.Manager()
    actual_projects = ProjectActualManager()

    def __str__(self):
        return f'{self.name} ({self.division.name} - {self.division.company.title})'
    

class ProjectStage(models.Model):
    """Этап проекта"""
    name        = models.CharField(max_length=255, help_text="Наименование", verbose_name="Наименование")

    class Meta:
        verbose_name = "Этап"
        verbose_name_plural = "Этапы"
   
    def __str__(self):
        return f'{self.name}'
    

class BusinessPlan(models.Model):
    """Бизнес план"""
    name        = models.CharField(max_length=250, help_text="Наименование", verbose_name="Наименование")
    date        = models.DateField(help_text="Дата бизнес плана", verbose_name='Дата бизнес плана')
    project     = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="businessplans", help_text="Проект", verbose_name="Проект")
    contacts    = models.TextField(blank=True, null=True, help_text="Контакты", verbose_name="Контакты")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')

    class Meta:
        verbose_name = "Бизнес план"
        verbose_name_plural = "Бизнес планы"

    def __str__(self):
        return f'{self.project.name}: {self.date} - {self.name}'
    

class BusinessPlanCostItem(models.Model):
    """Статья затрат"""
    name        = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = "Статья затрат"
        verbose_name_plural = "Статьи затрат"
   
    def __str__(self):
        return f'{self.name}'
    

class BusinessPlanFacility(models.Model):
    """Объект из Бизнес плана"""
    name        = models.CharField(max_length=255, help_text="Наименование", verbose_name="Наименование")
    project     = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="bpf", help_text="Проект", verbose_name="Проект")
    count       = models.IntegerField(blank=True, null=True, help_text="Количество", verbose_name="Количество")
    length      = models.FloatField(blank=True, null=True, help_text="Длина", verbose_name="Длина")
    square      = models.FloatField(blank=True, null=True, help_text="Площадь", verbose_name="Площадь")


    class Meta:
        verbose_name = "Объект в Бизнес плане"
        verbose_name_plural = "Объекты в Бизнес плане"

    def __str__(self):
        return f'{self.project.name}: {self.name}'
     

class BusinessPlanStr(models.Model):
    """Строка бизнес плана"""
    bp          = models.ForeignKey(BusinessPlan, on_delete=models.CASCADE, related_name="businessplanstr", help_text="Бизнес план", verbose_name="Бизнес план")
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="businessplanstr", help_text="Компания", verbose_name="Компания")
    bpf         = models.ForeignKey(BusinessPlanFacility, on_delete=models.CASCADE, related_name="businessplanstr", help_text="Объект из Бизнес плана", verbose_name="Объект из Бизнес плана")
    costitem    = models.ForeignKey(BusinessPlanCostItem, on_delete=models.CASCADE, related_name="businessplanstr", help_text="Статья затрат", verbose_name="Статья затрат")
    stage       = models.ForeignKey(ProjectStage, on_delete=models.SET_NULL, blank=True, null=True, related_name="businessplanstr", help_text="Этап", verbose_name="Этап")
    facility    = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="businessplanstr", help_text="Объект", verbose_name="Объект")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")

    class Meta:
        verbose_name = "Строка в бизнес плане"
        verbose_name_plural = "Строки в бизнес плане"

    def __str__(self):
        return f'{self.bp.name} \ {self.bpf.name} \ {self.costitem.name}'


class BPTask(models.Model):
    """Производство (задача согласно БП)"""
    bps         = models.ForeignKey('BusinessPlanStr', on_delete=models.CASCADE, related_name="tasks", help_text="Строка бизнес плана", verbose_name="Строка")
    name        = models.CharField(max_length=255, help_text="Наименование", verbose_name="Наименование")
    dpb         = models.DateField(default=timezone.now)
    dpe         = models.DateField()
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    
    class Meta:
        verbose_name = "Произодство"
        verbose_name_plural = "Произодства"

    def __str__(self):
        return f'{self.name}'
    

class PaymentBPTask(models.Model):
    """Оплата планируемая согласно Бизнес плана"""
    bptask       = models.ForeignKey(BPTask, on_delete=models.SET_NULL, blank=True, null=True, related_name="bppayments", help_text="Задача по бизнес плану", verbose_name="Задача по бизнес плану")
    date_develop = models.DateField(blank=True, null=True)  # Дата освоения
    date_funding = models.DateField(blank=True, null=True)  # Дата финансирования
    costp        = models.FloatField(default=0, validators=[MinValueValidator(0.00)])
    note         = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual       = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at   = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at   = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    contract     = models.ForeignKey(Contract, on_delete=models.SET_NULL, related_name="bppayments", blank=True, null=True, help_text="Договор", verbose_name="Договор")
    file         = models.ForeignKey(Document, on_delete=models.SET_NULL, blank=True, null=True, related_name="bppayments", help_text="Документ", verbose_name="Документ")

    class Meta:
        verbose_name = "Планируемая оплата"
        verbose_name_plural = "Планируемые оплаты"

    def __str__(self):
        return f'{self.bptask.name}'
    