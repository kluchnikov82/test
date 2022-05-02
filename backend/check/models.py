import uuid
from django.db import models


class Printer(models.Model):
    """
    Модель принтер
    """
    CHECK_TYPES = (
        ('kitchen', 'Кухня'),
        ('client', 'Клиент'),
    )
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255,
                            verbose_name='Название принтера',
                            blank=False)
    api_key = models.CharField(max_length=255,
                            verbose_name='Ключ доступа к API',
                            blank=False)
    check_type = models.CharField(max_length=255,
                               choices=CHECK_TYPES,
                               verbose_name='Тип чека',
                               blank=False)
    point_id = models.IntegerField(
                            default=0,
                            verbose_name='Точка к которой привязан принтер')

    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтера'
        db_table = 'printer'

    def __str__(self):
        return self.name


class Check(models.Model):
    """
    Модель чек
    """
    CHECK_TYPES = (
        ('kitchen', 'Кухня'),
        ('client', 'Клиент'),
    )
    STATUS_TYPES = (
        ('new', 'Новый'),
        ('rendered', 'Оказаный'),
        ('printed', 'Распечатаный')
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    printer_id = models.ForeignKey(Printer, on_delete=models.DO_NOTHING, null=True, default=None)
    type_check = models.CharField(max_length=255,
                            choices=CHECK_TYPES,
                            verbose_name='Тип чека',
                            default='kitchen',
                            blank=False)
    order = models.JSONField()
    status = models.CharField(max_length=255,
                              choices=STATUS_TYPES,
                              verbose_name='Статус чека',
                              default='new',
                              blank=False)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        db_table = 'check'

    def __str__(self):
        return self.uuid
