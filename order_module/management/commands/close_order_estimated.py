from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from order_module.models import Order, OrderStatus, PostingMethod


class Command(BaseCommand):
    help = 'کلس برای تغییر وضعیت سفارش'
    def handle(self ,*args ,**kwargs):
        now = timezone.now()
        finished_status = OrderStatus.objects.filter(title='پایان یافته').first()

        if not finished_status:
            print('no such a order status: پایان یافته')
            return
        total_orders = 0
        for pm in PostingMethod.objects.all():
            estimated = now - timedelta(days=pm.estimated_time)
            updated = Order.objects.filter(
                is_paid=True ,
                is_done=False ,
                payment_date__isnull=False ,
                posting_method=pm,
                status__title='ارسال شده',
                payment_date__lte=estimated
            ).update(
                is_done=True,
                status=finished_status
            )
            total_orders += updated

        print(f'nobakht nuts orders updated ({total_orders})')
