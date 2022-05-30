# Generated by Django 2.2.7 on 2019-11-25 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20191125_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='food_type',
            field=models.CharField(choices=[('Pizza', 'Pizza'), ('Pasta', 'Pasta'), ('Salad', 'Salad'), ('Platter', 'Platter'), ('Sub', 'Sub')], default=2, max_length=65),
            preserve_default=False,
        ),
    ]
