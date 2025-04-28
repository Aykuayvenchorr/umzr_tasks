import datetime
from django.utils import timezone
from django.db import models

from app_doc.models import Contract, Document
from app_econ.models import BusinessPlanCostItem, Project, BPTask
from app_struct.models import Company, Employee, Division, License, Facility
from django.core.validators import MinValueValidator


class Task(models.Model):
    """"Задача"""

    IMPORTANT_CHOICES = (
        ('low', 'Низкая'),
        ('middle', 'Средняя'),
        ('high', 'Высокая'),
    )

    STATUS = (
        ('not', 'Не начата'),
        ('worked', 'В работе'),
        ('canceled', 'Отмена'),
        ('ended', 'Завершена'),
    )

    parent      = models.ForeignKey('Task', on_delete=models.SET_NULL, blank=True, null=True)
    name        = models.CharField(max_length=100, blank=False, null=False)
    desc        = models.TextField(blank=True, null=True)
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")

    user_created = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_created')
    user_responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_responsible')
    user_ended  = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_ended')
    dt_created  = models.DateField(auto_now_add=True, help_text="Создана", verbose_name='Создана')
    dt_ended    = models.DateField(auto_now_add=True, help_text="Завершена", verbose_name='Завершена')

    importance  = models.CharField(max_length=50, choices=IMPORTANT_CHOICES, default='Средняя')
    status      = models.CharField(max_length=50, choices=STATUS)
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    documents = models.ManyToManyField('app_doc.Document', blank=True, related_name="tasks", help_text="Документы, связанные с этой задачей")

    company     = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    division    = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True)
    project     = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    license     = models.ForeignKey(License, on_delete=models.SET_NULL, blank=True, null=True)
    facility    = models.ForeignKey(Facility, on_delete=models.SET_NULL, blank=True, null=True)

    fact_fin_dt = models.DateField(help_text="Дата оплаты", verbose_name='Дата оплаты', blank=True, null=True)
    fact_fin_cost = models.FloatField(default=0, validators=[MinValueValidator(0.00)], blank=True, null=True)
    fact_dev_dt = models.DateField(help_text="Дата освоения", verbose_name='Дата освоения', blank=True, null=True)
    fact_dev_cost = models.FloatField(default=0, validators=[MinValueValidator(0.00)], blank=True, null=True)
    cost_info   = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")


    # costitem    = models.ForeignKey(BusinessPlanCostItem, on_delete=models.SET_NULL, blank=True, null=True)
    # payment_plan = models.ForeignKey('PaymentTaskPlan', on_delete=models.SET_NULL, blank=True, null=True, related_name="task", help_text="Плановая оплата", verbose_name="Плановая оплата")
    # level       = models.IntegerField()

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        # ordering = ["company", "division"]
        # indexes = [models.Index(fields=['user']), ]
        # Уникальные вместе
        # unique_together = ['field1', 'field2']

    def __str__(self):
        return f'{self.id} - {self.name}'
    

class PlanDateStart(models.Model):
    """Плановая дата начала задачи"""
    task        = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='plandatestart')
    dt_start    = models.DateField(help_text="Плановая дата начала", verbose_name='Плановая дата начала')
    note        = models.CharField(max_length=100, blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    user_created = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='plandatestart')
    dt_created  = models.DateField(auto_now_add=True, help_text="Создана", verbose_name='Создана')
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")

    class Meta:
        verbose_name = "Плановая дата начала задачи"
        verbose_name_plural = "Плановые даты начала задачи"

    def __str__(self):
        return f'{self.id} - {self.task} - {self.dt_start}'

class PlanDateEnd(models.Model):
    """Плановая дата завершения задачи"""
    task        = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='plandateend')
    dt_end = models.DateField(help_text="Плановая дата завершения", verbose_name='Плановая дата завершения')
    note     = models.CharField(max_length=100, blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    user_created = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='plandateend')
    dt_created  = models.DateField(auto_now_add=True, help_text="Создана", verbose_name='Создана')
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")

    class Meta:
        verbose_name = "Плановая дата завершения задачи"
        verbose_name_plural = "Плановые даты завершения задачи"

    def __str__(self):
        return f'{self.id} - {self.task} - {self.dt_end}'
    

class PlanCost(models.Model):
    """"Плановая оплата"""
    task        = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='plancost')
    plan_fin_dt = models.DateField(help_text="Плановая дата оплаты", verbose_name='Плановая дата оплаты', blank=True, null=True)
    plan_fin_cost = models.FloatField(default=0, blank=True, null=True, validators=[MinValueValidator(0.00)])
    plan_dev_dt = models.DateField(help_text="Плановая дата освоения", blank=True, null=True, verbose_name='Плановая дата освоения')
    plan_dev_cost = models.FloatField(default=0, blank=True, null=True, validators=[MinValueValidator(0.00)])
    nds = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(0.00)])
    ndfl = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(0.00)])

    class Meta:
        verbose_name = "Плановая оплата"
        verbose_name_plural = "Плановые оплаты"

    def __str__(self):
        return f'{self.id} - {self.task}'