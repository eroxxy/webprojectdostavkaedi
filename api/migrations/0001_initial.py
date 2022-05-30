# Generated by Django 4.0.4 on 2022-05-25 17:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSizeApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=65)),
            ],
        ),
        migrations.CreateModel(
            name='PizzaToppingApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='PizzaTypeApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='PizzaOrderApi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=65)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime(2022, 5, 25, 17, 1, 35, 261572))),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Ordered', 'Ordered'), ('Processing', 'Processing'), ('Sent', 'Sent'), ('Complete', 'Complete')], max_length=20)),
                ('price', models.IntegerField(default=0)),
                ('food_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizza', to='api.pizzatypeapi')),
                ('foodsize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizza', to='api.foodsizeapi')),
                ('toppings', models.ManyToManyField(blank=True, related_name='pizza', to='api.pizzatoppingapi')),
            ],
        ),
    ]
