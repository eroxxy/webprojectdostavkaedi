from csv import DictReader
from django.core.management import BaseCommand

from api.models import PizzaTypeApi, PizzaToppingApi


class Command(BaseCommand):
    help = "Loads data from children.csv"

    def handle(self, *args, **options):
        for row in DictReader(open('./pizza_and_toppings.csv')):
            PizzaTypeApi.objects.create(name=row["pizza"])
            PizzaToppingApi.objects.create(name=row["topping"])
        print("Upload Done!!!")