# Generated by Django 5.1.1 on 2024-12-18 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppCustomer', '0002_alter_customer_address_alter_customer_city_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SystemRole',
        ),
    ]
