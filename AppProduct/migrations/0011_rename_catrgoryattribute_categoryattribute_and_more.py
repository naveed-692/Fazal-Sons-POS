# Generated by Django 5.1.1 on 2024-11-27 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppProduct', '0010_delete_imagemodel'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CatrgoryAttribute',
            new_name='CategoryAttribute',
        ),
        migrations.RenameModel(
            old_name='SubCatrgoryAttribute',
            new_name='SubCategoryAttribute',
        ),
    ]
