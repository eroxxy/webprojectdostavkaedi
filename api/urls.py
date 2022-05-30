from django.template.defaulttags import url
from django.urls import include
from rest_framework import routers

from api.views import OrdersViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r'orders', OrdersViewSet)
urlpatterns = [
]

urlpatterns += router.urls