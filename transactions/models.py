from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Transaction(models.Model):

    class Category(models.TextChoices):
        FOOD          = 'FOOD',          'Pārtika un produkti'
        TRANSPORT     = 'TRANSPORT',     'Transports'
        HOUSING       = 'HOUSING',       'Mājoklis un komunālie pakalpojumi'
        HEALTH        = 'HEALTH',        'Veselība'
        ENTERTAINMENT = 'ENTERTAINMENT', 'Izklaide'
        SALARY        = 'SALARY',        'Alga'
        OTHER         = 'OTHER',         'Cits'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='Lietotājs',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Summa',
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
        verbose_name='Kategorija',
    )
    date = models.DateField(
        verbose_name='Datums',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Apraksts',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transakcija'
        verbose_name_plural = 'Transakcijas'
        ordering = ['-date', '-created_at']

    def clean(self):
        if self.amount is not None and self.amount < 0:
            raise ValidationError({'amount': 'Summa nevar būt negatīva.'})

    def __str__(self):
        return f'{self.get_category_display()} — {self.amount} EUR ({self.date})'