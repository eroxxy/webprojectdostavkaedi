from django.db import models
from datetime import datetime


class FoodSizeApi(models.Model):
    size = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.size}'


class PizzaTypeApi(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class PizzaToppingApi(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class PizzaOrderApi(models.Model):
    foodsize = models.ForeignKey(
        FoodSizeApi, on_delete=models.CASCADE, related_name='pizza')
    extra_toppings = models.ManyToManyField(
        PizzaToppingApi, blank=True, related_name='pizza')
    food_type = models.ForeignKey(
        PizzaTypeApi,  on_delete=models.CASCADE, related_name='pizza')
    user = models.CharField(max_length=65)
    date = models.DateTimeField(blank=True, default=datetime.now())
    status = models.CharField(max_length=20, choices=[
        ('Draft', 'Draft'),
        ('Ordered', 'Ordered'),
        ("Processing", "Processing"),
        ("Sent", "Sent"),
        ('Complete', 'Complete')
        ])
    price = models.IntegerField(default=0)
    is_favourite = models.BooleanField(default=False, verbose_name="Любимый заказ?")

    def __str__(self):
        return f'{self.pk} {self.user} {self.food_type}'


class UserFavouriteOrder(models.Model):
    class Meta:
        verbose_name = "Любимый заказ пользователя"
        verbose_name_plural = "Любимые заказы пользователей"

    user = models.CharField(max_length=65, verbose_name="Пользователь")
    order = models.OneToOneField(PizzaOrderApi, verbose_name="Любимый заказ", on_delete=models.CASCADE)
