# Generated by Django 5.1.2 on 2024-10-11 06:14

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile_alter_transaction_user_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='summ',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
