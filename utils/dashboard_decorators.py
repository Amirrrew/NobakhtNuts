from account_module.models import User
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
    total_week_sale = 0

    for i in range(7):
        day = week_start + timedelta(days=i)

        sale = (
            Order.objects.filter(
                is_paid=True,
                payment_date__date=day
            ).aggregate(total=Sum("finalized_price"))["total"] or 0
        )

        total_week_sale += sale
        max_sale = max(max_sale, sale)


        days.append({
            "day": day,
            "sale": sale,
        })


    data = {
        "days": days,
        "max_sale": max_sale,
        "total_week_sale": total_week_sale
    }
    return data


def get_sales_week_growth():
    now = timezone.now()

    current_week_start = now - timedelta(days=7)
    previous_week_start = now - timedelta(days=14)

    current_week = (
        Order.objects.filter(
            is_paid=True,
            payment_date__gte=current_week_start
        ).aggregate(total=Sum('finalized_price'))['total'] or 0
    )

    previous_week = (
        Order.objects.filter(
            is_paid=True,
            payment_date__gte=previous_week_start,
            payment_date__lt=current_week_start
        ).aggregate(total=Sum('finalized_price'))['total'] or 0
    )

    if previous_week == 0:
        percent = 100 if current_week > 0 else 0
    else:
        percent = round(((current_week - previous_week) / previous_week) * 100, 1)

    return {
        "percent": percent,
    }


def get_order_today():
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)

    today_orders = Order.objects.filter(
        is_paid=True,
        payment_date__date=today
    ).count()

    yesterday_orders = Order.objects.filter(
        is_paid=True,
        payment_date__date=yesterday
    ).count()

    yesterday_total = Order.objects.filter(
        is_paid=True,
        payment_date__date=yesterday
    ).aggregate(total=Sum('finalized_price'))['total'] or 0

    today_total = Order.objects.filter(
        is_paid=True,
        payment_date__date=today,
    ).aggregate(total=Sum('finalized_price'))['total'] or 0

    if yesterday_total == 0:
        percent = 100 if today_orders > 0 else 0
    else:
        percent = round(
            ((today_total - yesterday_total) / yesterday_total) * 100,
            1
        )


    return {
        "today_orders": today_orders,
        'today_total': today_total,
        'yesterday_total': yesterday_total,
        'percent': percent,
        "difference_orders": today_orders - yesterday_orders,
    }

def get_user_growth():
    all_users = User.objects.all()
    week_start = timezone.now() - timedelta(days=7)
    new_users = all_users.filter(created_at__gte=week_start)

    return  {
        'all_users': all_users,
        'new_users': new_users,
    }