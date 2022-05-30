from rest_framework import serializers

from api.models import PizzaOrderApi

from api.models import UserFavouriteOrder


class PizzaOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PizzaOrderApi
        fields = (
            "foodsize",
            "extra_toppings",
            "food_type",
            "user",
            "date",
            "status",
            "price",
            "is_favourite",
        )

    def validate(self, attrs):
        extra_toppings = attrs["extra_toppings"]
        if len(extra_toppings) > 3:
            raise serializers.ValidationError({"extra_toppings": "Дополнительных начинок не должно быть больше 3-х"})

        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.is_favourite:
            UserFavouriteOrder.objects.create(
                user=instance.user,
                order=instance.order,
            )
        return instance

class FavouriteOrderSerializer(serializers.Serializer):
    user = serializers.CharField()
    order_id = serializers.IntegerField()

    def validate(self, attrs):
        user = attrs["user"]
        order_id = attrs["order_id"]
        if not PizzaOrderApi.objects.filter(pk=order_id, user=user, is_favourite=True).exists():
            raise serializers.ValidationError({"order_id": {"Данный заказ не отмечен для данного пользователя как любимый"}})
        return attrs