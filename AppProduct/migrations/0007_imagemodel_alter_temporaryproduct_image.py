# Generated by Django 5.1.1 on 2024-11-24 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppProduct', '0006_rename_brand_name_product_brand_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'image_model',
            },
        ),
        migrations.AlterField(
            model_name='temporaryproduct',
            name='image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='TemProduct'),
        ),
    ]
