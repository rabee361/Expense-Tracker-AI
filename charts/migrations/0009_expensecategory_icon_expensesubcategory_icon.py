# Generated by Django 5.0.2 on 2024-07-30 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0008_alter_spendinglimit_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensecategory',
            name='icon',
            field=models.ImageField(null=True, upload_to='images/icons/categories'),
        ),
        migrations.AddField(
            model_name='expensesubcategory',
            name='icon',
            field=models.ImageField(null=True, upload_to='images/icons/subctegories'),
        ),
    ]
