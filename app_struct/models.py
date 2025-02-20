from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.

# Модель предприятия
class CompanyMainManager(models.Manager):
    """Менеджер компаний - только головные компании"""
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=True)
class Company(models.Model):
    """Таблица компаний"""
    title       = models.CharField(max_length=250, unique=True, help_text="Наименование", verbose_name="Наименование")
    name        = models.CharField(max_length=250, help_text="Полное наименование", verbose_name="Полное наименование")
    parent      = models.ForeignKey('Company', on_delete=models.SET_NULL, blank=True, null=True, related_name="subcompany", help_text="Головная компания", verbose_name="Головная")
    logo        = models.ImageField(blank=True, null=True, upload_to="struct/company/logo/", help_text="Логотип", verbose_name="Логотип")
    contacts    = models.TextField(blank=True, null=True, help_text="Контакты", verbose_name="Контакты")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуальна", verbose_name="Актуальна")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    gis         = models.CharField(max_length=255, blank=True, null=True, help_text="GIS ID", verbose_name="GIS ID")

    objects     = models.Manager()
    main        = CompanyMainManager()

    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"
        ordering = ["title", ]
        indexes = [models.Index(fields=['title']), ]
        # Уникальные вместе
        # unique_together = ['field1', 'field2']

    def __str__(self):
        return self.title
    

# Модель подразделения
class DivisionMainManager(models.Manager):
    """Менеджер подразделений - только верхнеуровневые подразделения"""
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=True)
class Division(models.Model):
    """Подразделения Компании"""
    company     = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="divisions", help_text="Компания", verbose_name="Компания")
    name        = models.CharField(max_length=250, help_text="Наименование", verbose_name="Наименование")
    abbr        = models.CharField(max_length=17, help_text="Аббревиатура", verbose_name="Аббревиатура")
    parent      = models.ForeignKey('Division', on_delete=models.SET_NULL, blank=True, null=True, related_name="subdivisions", help_text="Руководящее подразделение", verbose_name="Руководящее")
    contacts    = models.TextField(blank=True, null=True, help_text="Контакты", verbose_name="Контакты")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')

    objects     = models.Manager()
    main        = DivisionMainManager()

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        ordering = ["company", "name"]
        indexes = [models.Index(fields=['name']), ]
        unique_together = (('company', 'name'), ('company', 'abbr'))

    def __str__(self):
        return f'{self.abbr} ({self.company.title})'


# Модель сотрудника
class Employee(models.Model):
    """Модель сотрудника предприятия"""
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL, help_text="Пользователь системы", verbose_name='Пользователь')
    name        = models.CharField(max_length=250, help_text="Имя", verbose_name="Имя")
    surname     = models.CharField(max_length=250, help_text="Фамилия", verbose_name="Фамилия")
    patronymic  = models.CharField(max_length=250, help_text="Отчество", verbose_name="Отчество", blank=True, null=True)
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees", help_text="Компания", verbose_name="Компания")
    division    = models.ForeignKey(Division, on_delete=models.CASCADE, blank=True, null=True, related_name="employees", help_text="Подразделение", verbose_name="Подразделение")
    post        = models.CharField(max_length=250, help_text="Должность", verbose_name="Должность")
    phone       = models.CharField(max_length=250, help_text="Телефон", verbose_name="Телефон")
    email       = models.EmailField(max_length=250, help_text="Электронная почта", verbose_name="Почта", blank=True, null=True)
    avatar      = models.ImageField(upload_to='struct/employee/ava/', blank=True, null=True, help_text="Аватар", verbose_name="Аватар")
    is_director = models.BooleanField(default=False, help_text="Руководитель", verbose_name="Руководитель")
    date_birth  = models.DateField(blank=True, null=True, help_text="Дата рождения", verbose_name="Дата рождения")
    contacts    = models.TextField(blank=True, null=True, help_text="Контактная информация", verbose_name="Контакт")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["surname", "name", "patronymic"]
        indexes = [models.Index(fields=['surname']), ]
        unique_together = (('surname', 'name', "patronymic", "company", "post"), )

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic} ({self.post} {self.company.title})'


# Модель лицензии
class LicenseActualManager(models.Manager):
    """Менеджер актуальных лицензий - только актуальные лицензии"""
    def get_queryset(self):
        return super().get_queryset().filter(actual=True)   
class License(models.Model):
    """Лицензионные участки"""
    name        = models.CharField(max_length=250, unique=True, help_text="Наименование", verbose_name="Наименование")
    owner       = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, related_name="licenses", help_text="Владелец", verbose_name="Владелец")
    dt_start    = models.DateField(help_text="Начало", verbose_name='Начало')
    dt_end      = models.DateField(help_text="Окончание", verbose_name='Окончание')
    doc         = models.FileField(blank=True, null=True, upload_to="doc/license/", help_text="Файл лицензии", verbose_name="Лицензия")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    gis         = models.CharField(max_length=255, blank=True, null=True, help_text="GIS ID", verbose_name="GIS ID")

    objects     = models.Manager()
    actuals     = LicenseActualManager()

    class Meta:
        verbose_name = "Лицензия"
        verbose_name_plural = "Лицензии"
        ordering = ["owner", "name"]
        indexes = [models.Index(fields=['name']), ]

    def __str__(self):
        return f'{self.name}'


# Модель объекта
class FacilityMainManager(models.Manager):
    """Менеджер объектов - только верхнеуровневые объекты"""
    def get_queryset(self):
        return super().get_queryset().filter(parent__isnull=True)
class FacilityActualManager(models.Manager):
    """Менеджер объектов - только актуальные объекты"""
    def get_queryset(self):
        return super().get_queryset().filter(actual=True)
class FacilityMainActualManager(models.Manager):
    """Менеджер объектов - только верхнеуровневые и актуальные объекты"""
    def get_queryset(self):
        return super().get_queryset().filter(Q(parent__isnull=True) & Q(actual=True))
class FacilityType(models.Model):
    """Типы объектов"""
    name = models.CharField(max_length=255, help_text="Тип объекта", verbose_name="Тип объекта", unique=True)

    class Meta:
        verbose_name = "Тип объекта"
        verbose_name_plural = "Типы объектов"
        ordering = ['name', ]

    def __str__(self):
        return f'{self.name}'    
class Facility(models.Model):
    """Объекты месторождения"""
    name        = models.CharField(max_length=255, help_text="Наименование", verbose_name="Наименование")
    license     = models.ForeignKey('License', on_delete=models.SET_NULL, blank=True, null=True, related_name="facilities", help_text="Лицензия", verbose_name="Лицензия")
    parent      = models.ForeignKey('Facility', on_delete=models.SET_NULL, blank=True, null=True, related_name="facilities", help_text="Основной объект", verbose_name="Основной объект")
    type        = models.ForeignKey('FacilityType', on_delete=models.SET_NULL, blank=True, null=True, related_name="facilities", help_text="Тип объекта", verbose_name="Тип объекта")
    count       = models.FloatField(blank=True, null=True, help_text="Количество", verbose_name="Количество")
    length      = models.FloatField(blank=True, null=True, help_text="Протяженность", verbose_name="Протяженность")
    square      = models.FloatField(blank=True, null=True, help_text="Площадь", verbose_name="Площадь")
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    gis         = models.CharField(blank=True, null=True, help_text="GIS ID", verbose_name="GIS ID")
    gist        = models.CharField(blank=True, null=True, help_text="Таблица в GIS", verbose_name="Таблица в GIS")

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        ordering = ['license', 'name']
        indexes = [models.Index(fields=['name']), ]
        unique_together = ('license', 'parent', 'name')

    def __str__(self):
        return f'{self.name} ({self.license.name})'

