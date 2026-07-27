from datetime import timedelta
from sys import exception

from django.utils import timezone

from django.core.management import BaseCommand

from order_module.models import Order


class Command(BaseCommand):
    help = 'آزادسازی موجودی رزروشده برای سفارشاتی که پرداختشون تکمیل نشد'
    def handle(self, *args, **kwargs):
        now = timezone.now()
        estimated_time = now - timedelta(minutes=15)
        orders = Order.objects.filter(
            is_done=False,
            is_paid=False,
            stock_reserved=True,
            stock_reservation_time__lte=estimated_time,
        )

        drop_count = 0
        failed = 0

        for order in orders:
            try:
                order.drop_reservation()
                drop_count+=1
            except Exception as e:
                failed+=1
                print(f'failed:{failed} ---- {e}')

        print(f'drop_count:{drop_count}\n failed: {failed}')