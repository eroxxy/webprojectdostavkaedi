# Generated by Django 4.0.4 on 2022-05-25 17:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_pizzaorderapi_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pizzaorderapi',
            old_name='toppings',
            new_name='extra_toppings',
        ),
        migrations.AlterField(
            model_name='pizzaorderapi',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 25, 17, 9, 43, 43448)),
        ),
    ]