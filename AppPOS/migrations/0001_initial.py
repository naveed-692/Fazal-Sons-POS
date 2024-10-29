# Generated by Django 5.1.1 on 2024-10-28 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AppCustomer', '0005_systemrole'),
        ('AppProduct', '0030_alter_product_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_code', models.CharField(max_length=100, null=True, unique=True)),
                ('status', models.CharField(blank=True, null=True)),
                ('purchase_date', models.CharField(blank=True, null=True)),
                ('payment_type', models.CharField(blank=True, null=True)),
                ('invoice_amount', models.CharField(blank=True, null=True)),
                ('discount', models.CharField(blank=True, null=True)),
                ('grand_total', models.CharField(blank=True, null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('created_by', models.CharField(max_length=200, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('updated_by', models.CharField(max_length=200, null=True)),
                ('cust_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppCustomer.customer', to_field='cust_code')),
            ],
            options={
                'db_table': 'tbl_purchase_invoice',
            },
        ),
        migrations.CreateModel(
            name='PurchaseInvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_item_code', models.CharField(max_length=100, null=True, unique=True)),
                ('status', models.CharField(blank=True, null=True)),
                ('quantity', models.CharField(blank=True, null=True)),
                ('cost', models.CharField(blank=True, null=True)),
                ('item_total', models.CharField(blank=True, null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('created_by', models.CharField(max_length=200, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('invoice_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppPOS.purchaseinvoice', to_field='invoice_code')),
                ('sku', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppProduct.product', to_field='sku')),
            ],
            options={
                'db_table': 'tbl_purchase_invoice_item',
            },
        ),
    ]
