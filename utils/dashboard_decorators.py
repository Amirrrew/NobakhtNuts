from order_module.models import Order
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum



today = timezone.localdate()

def get_sales_week():
    weekday = (today.weekday() + 2) % 7
    week_start = today - timedelta(days=weekday)

    days = []
    max_sale = 0

    for i in range(7):
        day = week_start + timedelta(days=i)

        sale = (
            Order.objects.filter(
                is_paid=True,
                payment_date__date=day
            ).aggregate(total=Sum("finalized_price"))["total"] or 0
        )

        days.append({
            "day": day,
            "sale": sale,
        })

        max_sale = max(max_sale, sale)

    context = {
        "days": days,
        "max_sale": max_sale,
    }
    return context


def get_all_order_count():
    orders = Order.objects.filter(
        is_paid=True,
    ).count()

    return orders

def get_order_today():
    orders = Order.objects.filter(
        is_paid=True ,
        payment_date__date=today
    ).count()

    return orders