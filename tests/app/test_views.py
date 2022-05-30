import pytest

from django.contrib.auth.models import User
from orders.models import PizzaTopping
from orders.models import Price

@pytest.mark.django_db
def test_index(client, user, pizza_topping, price_1):
    client.force_login(user)
    resp = client.get("")
   
    assert resp.status_code == 200
    assert resp.context["user"] == user
    assert resp.context["basket"] == []
    assert resp.context["basket_total"] == 0
    assert resp.context["checkout"] == {"Pizzas": []}
    assert resp.context["menu"] == {"Pizzas": [str(i) for i in Price.objects.all() if i.food_type == 'Pizza'],}


@pytest.mark.django_db
def test_login_fail(client, user):
    resp = client.post("/login/", 
        {
            "username": user.username, 
            "password": 321,
        }
    )
    assert resp.context["message"] == 'Invalid credentials.'
    assert resp.status_code == 200


@pytest.mark.django_db
def test_logout(client, user):
    client.force_login(user)
    resp = client.get("/logout/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_register(client):
    attrs = {
        "username": "pizza_hunter",
        "password": "1234",
        "first_name": "Name",
        "last_name": "Surname",
        "email": "test@mail.ru",
    }
    resp = client.post("/register/", attrs)
    print(resp)
    created_user = User.objects.all()

    assert created_user.count() == 1
    assert created_user.first().username == "pizza_hunter"

    assert resp.status_code == 302
