# Generated by Django 3.1.7 on 2021-03-30 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='id',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='status',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='orderId',
            field=models.AutoField(default=-2, primary_key=True, serialize=False, unique=True),
            preserve_default=False,
        ),
    ]