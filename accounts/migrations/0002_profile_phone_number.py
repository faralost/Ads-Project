# Generated by Django 4.0.5 on 2022-06-25 02:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Введите номер телефона в формате +996 ХХХ ХХХ ХХХ', regex='^\\+[9]{2}?[6] [0-9]{3} [0-9]{3} [0-9]{3}$')], verbose_name='Номер телефона'),
            preserve_default=False,
        ),
    ]
