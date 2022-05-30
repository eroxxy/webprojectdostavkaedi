import datetime

from django.core.management import BaseCommand
from django.db.models import Sum
from django.utils import timezone

from api.models import PizzaOrderApi


class Command(BaseCommand):
    def add_arguments(self, parser):  # type: ignore
        parser.add_argument("--period", type=str, required=True)

    def handle(self, *args, **options):  # type: ignore
        period = options["period"]
        today = datetime.datetime.today()
        end_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=23, minute=59,
                                     second=59)
        if period == "day":
            start_date = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0,
                                           second=0)
            profit_dict = PizzaOrderApi.objects.filter(date__range=(start_date, end_date)).aggregate(profit=Sum("price"))
            print("Сегодняшняя прибыль равна: ", profit_dict["profit"])
        elif period == "month":
            start_date = datetime.datetime(year=today.year, month=today.month, day=1, hour=0, minute=0,
                                           second=0)
            profit_dict = PizzaOrderApi.objects.filter(date__range=(start_date, end_date)).aggregate(
                profit=Sum("price"))
            print("прибыль за месяц (с 1-го числа до сегодняшнего дня): ", profit_dict["profit"])
