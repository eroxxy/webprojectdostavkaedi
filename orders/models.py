from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class FoodSize(models.Model):
    size = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.size}'


class PizzaType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

class PizzaTopping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

class PizzaOrder(models.Model):
    foodsize = models.ForeignKey(
        FoodSize, on_delete=models.CASCADE, related_name='pizza')
    toppings = models.ManyToManyField(
        PizzaTopping, blank=True, related_name='pizza')
    food_type = models.ForeignKey(
        PizzaType,  on_delete=models.CASCADE, related_name='pizza')
    user = models.CharField(max_length=65)
    date = models.DateTimeField(blank=True, default=datetime.now())
    status = models.CharField(max_length=20, choices=[
        ('Draft', 'Draft'),
        ('Ordered', 'Ordered'),
        ("Processing", "Processing"),
        ("Sent", "Sent"),
        ('Complete', 'Complete')
        ])
    reg_pizza_type = models.CharField(max_length=65)

    @property
    def get_price(self):
        topping_count = self.toppings.count()
        if topping_count > 3:
            raise ValidationError("You can't select more than three toppings")
        if topping_count == 0:
            if self.foodsize.size == 'Small':
                price = Price.objects.get(
                    menu_item=f'{self.food_type} Pizza {self.reg_pizza_type}', food_type='Pizza').small
            elif self.foodsize.size == 'Large':
                price = Price.objects.get(
                    menu_item=f'{self.food_type} Pizza {self.reg_pizza_type}', food_type='Pizza').large
        elif self.foodsize.size == 'Small':
            price = Price.objects.get(
                menu_item=f'{self.food_type} Pizza {topping_count} Topping', food_type='Pizza').small
        elif self.foodsize.size == 'Large':
            price = Price.objects.get(
                menu_item=f'{self.food_type} Pizza {topping_count} Topping', food_type='Pizza').large
        else:
            price = 'none'
        return price

    def __str__(self):
        toppings = ", ".join(str(seg) for seg in self.toppings.all())
        return f'{self.foodsize} {self.food_type} with {toppings} Price: {self.get_price}'

class Price(models.Model):
    menu_item = models.CharField(max_length=65)
    food_type = models.CharField(max_length=65, choices=[
        ('Pizza', 'Pizza'),
        ('Topping', 'Topping')
    ])
    small = models.DecimalField(max_digits=10, decimal_places=2)
    large = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.menu_item}'
