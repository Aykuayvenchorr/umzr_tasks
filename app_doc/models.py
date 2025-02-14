from django.db import models

from app_struct.models import Company

class Contractor(models.Model):
    """Контрагент"""
    name        =  models.CharField(max_length=100, blank=True, null=True)
    esk         =  models.CharField(max_length=100, blank=True, null=True)
    company     =  models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, related_name="contractor", help_text="Компания", verbose_name="Компания")

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"

    def __str__(self):
        return f'{self.name} - {self.esk}'
    

class Contract(models.Model):
    """"Договор"""
    file        =  models.ForeignKey('Document', on_delete=models.SET_NULL, blank=True, null=True, related_name="contract", help_text="Документ", verbose_name="Документ")
    contractor   = models.ForeignKey('Contractor', on_delete=models.SET_NULL, blank=True, null=True, related_name="contract", help_text="Контрагент", verbose_name="Контрагент")

    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"

    def __str__(self):
        return f'{self.file} ({self.contractor})'
    

class FileType(models.Model):
    """Тип файла"""
    title       = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Тип файла"
        verbose_name_plural = "Типы файлов"

    def __str__(self):
        return f'{self.title}'
    

class Document(models.Model):
    """Документ"""
    title       = models.CharField(max_length=255)
    number      = models.CharField(max_length=255)
    file        = models.FileField(upload_to='tasks/', help_text="Загрузите документ")
    actual      = models.BooleanField(default=True, help_text="Актуально", verbose_name="Актуально")
    created_at  = models.DateTimeField(auto_now_add=True, help_text="Создан", verbose_name='Создан')
    updated_at  = models.DateTimeField(auto_now=True, help_text="Обновлен", verbose_name='Обновлен')
    note        = models.TextField(blank=True, null=True, help_text="Примечание", verbose_name="Примечание")
    type        = models.ForeignKey(FileType, on_delete=models.SET_NULL, blank=True, null=True, related_name="documents", help_text="Тип файла", verbose_name="Тип файла")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return f'{self.title} - {self.number}'

