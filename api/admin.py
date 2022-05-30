from api.models import PizzaOrderApi, FoodSizeApi, PizzaTypeApi, PizzaToppingApi
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


class PizzaOrderApiResource(resources.ModelResource):
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


class PizzaOrderApiAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = PizzaOrderApiResource

admin.site.register(FoodSizeApi)
admin.site.register(PizzaTypeApi)
admin.site.register(PizzaToppingApi)
admin.site.register(PizzaOrderApi,PizzaOrderApiAdmin)
