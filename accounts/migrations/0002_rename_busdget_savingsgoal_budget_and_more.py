# Generated by Django 5.0.2 on 2024-06-20 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savingsgoal',
            old_name='busdget',
            new_name='budget',
        ),
        migrations.AlterField(
            model_name='savingsgoal',
            name='notes',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
