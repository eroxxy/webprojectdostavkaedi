import pytest 
from orders.models import Price

@pytest.fixture
def price_1():
    return Price.objects.create(
        menu_item="Chicken Parm",
        food_type="Pizza",
        small=100.0,
        large=150.0,
    )