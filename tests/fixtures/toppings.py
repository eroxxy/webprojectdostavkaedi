import pytest 
from orders.models import PizzaTopping

@pytest.fixture
def pizza_topping():
    return PizzaTopping.objects.create(
        name="mashroom"
    )