# Generated by Django 5.0.2 on 2024-06-24 11:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_codeverification_otpcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='budget',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='account',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]