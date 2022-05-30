from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from api.models import PizzaOrderApi
from api.serializers import PizzaOrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import FavouriteOrderSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = PizzaOrderApi.objects.all()
    serializer_class = PizzaOrderSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['user']

    def get_serializer_class(self):
        if self.action == "repeat_favourite":
            return FavouriteOrderSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        qs = self.queryset
        food_type = self.request.query_params.get('food_type')
        if food_type:
            qs = qs.filter(food_type=food_type)
        return qs

    @action(methods=['POST'], detail=True, name="repeat_favourite")
    def repeat_favourite(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data={"user": instance.user, "order_id": instance.pk}, partial=partial)
        if serializer.is_valid(raise_exception=True):
            order = PizzaOrderApi.objects.create(
                foodsize=instance.foodsize,
                food_type=instance.food_type,
                user=instance.user,
                date=instance.date,
                status=instance.status,
                price=instance.price,
            )

            for topping in instance.extra_toppings.all():
                order.extra_toppings.set([topping])

        return Response({})

    @action(methods=['GET'], detail=False)
    def with_extra_toppings(self, request, *args, **kwargs):
        qs = PizzaOrderApi.objects.filter(extra_toppings__isnull=False)
        serializer = PizzaOrderSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def left_the_pizzeria(self, request, *args, **kwargs):
        qs = PizzaOrderApi.objects.filter(Q(status="Sent") | Q(status="Complete"))
        serializer = PizzaOrderSerializer(qs, many=True)
        return Response(serializer.data)
