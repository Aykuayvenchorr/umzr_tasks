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
        ('Низкая', 'Низкая'),
        ('Средняя', 'Средняя'),
        ('Высокая', 'Высокая'),
    )

    STATUS = (
        ('Не начата', 'Не начата'),
        ('В работе', 'В работе'),
        ('Отмена', 'Отмена'),
        ('Завершена', 'Завершена'),
    )

    parent      = models.ForeignKey('Task', on_delete=models.SET_NULL, blank=True, null=True)
    name        = models.CharField(max_length=100, blank=False, null=False)
    desc        = models.TextField(blank=True, null=True)

    term        = models.PositiveSmallIntegerField(default=0)  # Продолжительность в днях !!!
    dfb         = models.DateField(blank=True, null=True)
    dfe         = models.DateField(blank=True, null=True)

    importance  = models.CharField(max_length=50, choices=IMPORTANT_CHOICES, default='Средняя')
    status      = models.CharField(max_length=50, choices=STATUS)
    user_created = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_usc')
    user_responsible = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_usr')
    user_ended  = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks_use')

    company     = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True)
    division    = models.ForeignKey(Division, on_delete=models.SET_NULL, blank=True, null=True)
    project     = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    license     = models.ForeignKey(License, on_delete=models.SET_NULL, blank=True, null=True)
    facility    = models.ForeignKey(Facility, on_delete=models.SET_NULL, blank=True, null=True)

    costitem    = models.ForeignKey(BusinessPlanCostItem, on_delete=models.SET_NULL, blank=True, null=True)

    costf        = models.FloatField(default=0, validators=[MinValueValidator(0.00)])


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
    
    

class TermPlanTask(models.Model):
    """Плановые даты задачи"""
    task        = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name="termplan", help_text="Задача", verbose_name="Задача")
    dpb         = models.DateField(default=timezone.now)
    dpe         = models.DateField(default=timezone.now)
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')

    class Meta:
        verbose_name = "Плановые даты задачи"
        verbose_name_plural = "Плановые даты задачи"

    def __str__(self):
        return f'{self.task.name}'


class PaymentTaskPlan(models.Model):
    """Оплата планируемая"""
    task         = models.ForeignKey(Task, on_delete=models.SET_NULL, blank=True, null=True, related_name="payments", help_text="Задача", verbose_name="Задача")
    date_develop = models.DateField(blank=True, null=True)  # Дата освоения
    date_funding = models.DateField(blank=True, null=True)  # Дата финансирования
    costp        = models.FloatField(default=0, validators=[MinValueValidator(0.00)])
    note         = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual       = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at   = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at   = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    contract     = models.ForeignKey(Contract, on_delete=models.SET_NULL, blank=True, null=True, help_text="Договор", verbose_name="Договор")
    file         = models.ForeignKey(Document, on_delete=models.SET_NULL, blank=True, null=True, related_name="payplan", help_text="Документ", verbose_name="Документ")

    class Meta:
        verbose_name = "Планируемая оплата"
        verbose_name_plural = "Планируемые оплаты"

    def __str__(self):
        return f'{self.task.name}'




