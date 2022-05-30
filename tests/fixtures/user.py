import pytest 

from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create(
        username="Admin",
        password="123",
        is_active=True,
        is_staff=True
    )
    