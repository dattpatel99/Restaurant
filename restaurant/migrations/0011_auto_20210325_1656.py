# Generated by Django 3.1.7 on 2021-03-25 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0010_items_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Items',
            new_name='Item',
        ),
    ]