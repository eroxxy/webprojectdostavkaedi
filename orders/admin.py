# from dataclasses import field
# from django.contrib import admin
#
# from orders.models import FoodSize, PizzaType, PizzaTopping, PizzaOrder, Price
#
# from import_export import resources
# from orders.models import Price
# # from import_export.admin import ImportExportModelAdmin
# from import_export.admin import ImportExportActionModelAdmin
#
#
# class PriceResource(resources.ModelResource):
#
#     class Meta:
#         model = Price
#         fields = (
#             "menu_item",
#             "food_type",
#             "small",
#             "large",
#         )
#
#         export_fields = (
#             "menu_item",
#             "food_type",
#             "small",
#             "large",
#         )
#
#
# class PriceAdmin(ImportExportActionModelAdmin):
#     resource_class = PriceResource
#
#
#
# # Register your models here.
# admin.site.register(Price, PriceAdmin)
# admin.site.register(FoodSize)
# admin.site.register(PizzaType)
# admin.site.register(PizzaTopping)
# admin.site.register(PizzaOrder)
