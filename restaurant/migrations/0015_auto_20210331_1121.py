# Generated by Django 3.1.7 on 2021-03-31 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0014_auto_20210331_0246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='items_list',
            new_name='list',
        ),
    ]
