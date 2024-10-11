from decimal import Decimal

from django.db import models
from django.core.validators import EmailValidator, MinValueValidator


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Transaction(models.Model):
    class TypeOfTransaction(models.TextChoices):
        __slots__ = ()
        INCOME = ("INCOME", "Доход")
        EXPENSE = ("EXPENSE", "Расход")

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    summ = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.CharField(max_length=10, choices=TypeOfTransaction.choices)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.summ} {self.user} {self.category}"
