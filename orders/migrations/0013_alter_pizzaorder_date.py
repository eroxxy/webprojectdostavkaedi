# Generated by Django 4.0.4 on 2022-05-25 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_pizzaorder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizzaorder',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 25, 17, 9, 43, 36649)),
        ),
    ]