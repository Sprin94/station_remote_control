from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Station(models.Model):
    """Модель, описывающая станцию."""

    name = models.CharField(
        verbose_name='Название станции',
        max_length=50,
        db_index=True
    )

    class Status(models.TextChoices):
        RUNNING = ('running', 'исправная')
        BROKEN = ('broken', 'неисправна')

    status = models.CharField(
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.RUNNING,
        max_length=10,
        )
    create_data = models.DateTimeField(
        verbose_name='Дата создания станции',
        auto_now_add=True,
    )
    broken_data = models.DateTimeField(
        verbose_name='Дата поломки станции',
        null=True
    )

    def __str__(self):
        return self.name


class Directive(models.Model):
    """Модель, содержащая параметры указания передвижения станции."""

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='directives',
    )
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name='directives',
    )

    class CoordinatChoice(models.TextChoices):
        X = 'x', 'x'
        Y = 'y', 'y'
        Z = 'z', 'z'

    axis = models.CharField(
        'Направление',
        choices=CoordinatChoice.choices,
        max_length=1
    )
    distance = models.BigIntegerField(
        verbose_name='Дистанция'
    )


class Coordinate(models.Model):
    """Координаты станции."""

    station = models.ForeignKey(
        Station,
        verbose_name='Станция',
        related_name='coordinates',
        on_delete=models.CASCADE,
    )
    x = models.BigIntegerField(default=100)
    y = models.BigIntegerField(default=100)
    z = models.BigIntegerField(default=100)
