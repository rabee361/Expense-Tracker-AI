# Generated by Django 5.0.2 on 2024-08-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_type',
        ),
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(default='test', max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AccountType',
        ),
    ]
