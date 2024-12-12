# Generated by Django 5.1.1 on 2024-12-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppStock', '0002_remove_stock_sku'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='size',
        ),
        migrations.AddField(
            model_name='stock',
            name='sku',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
