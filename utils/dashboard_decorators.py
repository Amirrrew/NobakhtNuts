from datetime import datetime, time, timedelta

from django.db.models import (
    Sum,
    Count,
    Q,
    F,
    Case,
    When,
    DecimalField,
    IntegerField,
    FloatField,
    ExpressionWrapper,
)
import jdatetime
from django.db.models.functions import Coalesce
from django.utils import timezone
import calendar
from account_module.models import User
from order_module.models import Order, OrderStatus
from product_module.models import Product, ProductCategory
from support_module.models import Ticket

today = timezone.localdate()

def get_sales_week():
    today = timezone.localdate()

    week_start = today - timedelta(days=today.weekday())

    days = []
    total_week_sale = 0
    max_sale = 0

    for i in range(7):
        current_day = week_start + timedelta(days=i)

        start = timezone.make_aware(
            datetime.combine(current_day, time.min)
        )

        end = timezone.make_aware(
            datetime.combine(current_day, time.max)
        )

        sale = (
            Order.objects.filter(
                is_paid=True,
                payment_date__range=(start, end)
            ).aggregate(
                total=Coalesce(
                    Sum("finalized_price"),
                    0
                )
            )["total"]
        )

        total_week_sale += sale
        max_sale = max(max_sale, sale)

        days.append({
            "day": current_day,
            "sale": sale
        })

    return {
        "days": days,
        "max_sale": max_sale,
        "total_week_sale": total_week_sale,
    }


def get_sales_week_growth():
    now = timezone.now()

    current = now - timedelta(days=7)
    previous = now - timedelta(days=14)

    current_total = (
        Order.objects.filter(
            is_paid=True,
            payment_date__gte=current,
        ).aggregate(
            total=Coalesce(
                Sum("finalized_price"),
                0
            )
        )["total"]
    )

    previous_total = (
        Order.objects.filter(
            is_paid=True,
            payment_date__gte=previous,
            payment_date__lt=current,
        ).aggregate(
            total=Coalesce(
                Sum("finalized_price"),
                0
            )
        )["total"]
    )

    if previous_total == 0:
        percent = 100 if current_total else 0
    else:
        percent = round(
            ((current_total - previous_total) / previous_total) * 100,
            1,
        )

    return {
        "current": current_total,
        "previous": previous_total,
        "percent": percent,
    }


def get_order_today():
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)

    today_start = timezone.make_aware(datetime.combine(today, time.min))
    today_end = timezone.make_aware(datetime.combine(today, time.max))

    yesterday_start = timezone.make_aware(datetime.combine(yesterday, time.min))
    yesterday_end = timezone.make_aware(datetime.combine(yesterday, time.max))

    today_orders = Order.objects.filter(
        is_paid=True,
        payment_date__range=(today_start, today_end),
    )

    yesterday_orders = Order.objects.filter(
        is_paid=True,
        payment_date__range=(yesterday_start, yesterday_end),
    )

    today_count = today_orders.count()
    yesterday_count = yesterday_orders.count()

    today_total = today_orders.aggregate(
        total=Coalesce(Sum("finalized_price"), 0)
    )["total"]

    yesterday_total = yesterday_orders.aggregate(
        total=Coalesce(Sum("finalized_price"), 0)
    )["total"]

    if yesterday_total == 0:
        percent = 100 if today_total else 0
    else:
        percent = round(
            ((today_total - yesterday_total) / yesterday_total) * 100,
            1,
        )

    return {
        "today_orders": today_count,
        "today_total": today_total,
        "yesterday_total": yesterday_total,
        "difference_orders": today_count - yesterday_count,
        "percent": percent,
    }

def get_new_orders():
    return (
        Order.objects.filter(
            is_paid=True,
            is_done=False,
        )
        .select_related("user")
        .order_by("-payment_date")
    )

def get_user_growth():
    week = timezone.now() - timedelta(days=7)

    return {
        "all_users": User.objects.all().count(),
        "new_users": User.objects.filter(
            created_at__gte=week
        ).count(),
    }

def get_lowstock_products(count):
    return (
        Product.objects.filter(
            quantity__gt=0,
            quantity__lte=10,
        )
        .order_by("quantity")[:count]
    )


def get_best_selling_products(count):
    return (
        Product.objects.prefetch_related("product_image")
        .annotate(
            sold_count=Coalesce(
                Sum(
                    "orderdetail__count",
                    filter=Q(orderdetail__order__is_paid=True),
                ),
                0,
            ),
            sold_weight=Sum(
                ExpressionWrapper(
                    F("orderdetail__count") * F("orderdetail__pack_size__size"),
                    output_field=DecimalField(max_digits=20, decimal_places=2),
                ),
                filter=Q(orderdetail__order__is_paid=True),
            )
        )
        .annotate(
            sort_value=Case(
                When(is_byWeight=True, then=F("sold_weight")),
                default=F("sold_count"),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            )
        )
        .order_by("-sort_value")[:count]
    )


def get_new_tickets():
    new_tickets = Ticket.objects.filter(
        is_closed=False,
    ).order_by('-created_at' ,'-status')
    return new_tickets



def get_sales_month():

    today = timezone.localdate()

    j_today = jdatetime.date.fromgregorian(date=today)

    first_j = jdatetime.date(j_today.year, j_today.month, 1)
    first_day = first_j.togregorian()

    if j_today.month == 12:
        next_j = jdatetime.date(j_today.year + 1, 1, 1)
    else:
        next_j = jdatetime.date(j_today.year, j_today.month + 1, 1)

    next_month = next_j.togregorian()


    days = []
    total_month_sale = 0
    max_sale = 0

    current = first_day

    while current < next_month:

        start = timezone.make_aware(
            datetime.combine(current, time.min)
        )

        end = timezone.make_aware(
            datetime.combine(current, time.max)
        )

        sale = Order.objects.filter(
            is_paid=True,
            payment_date__range=(start, end)
        ).aggregate(
            total=Coalesce(
                Sum("finalized_price"),
                0
            )
        )["total"]


        total_month_sale += sale
        max_sale = max(max_sale, sale)

        days.append({
            "day": current,
            "sale": sale
        })

        current += timedelta(days=1)


    return {
        "days": days,
        "max_sale": max_sale,
        "total_month_sale": total_month_sale
    }

def get_category_chart():
    categories = (
        ProductCategory.objects
        .annotate(
            products_count=Count("subcategory__products")
        )
        .order_by("-products_count")
    )

    max_count = max(
        [c.products_count for c in categories],
        default=1
    )

    return {
        "categories": categories,
        "max_count": max_count,
    }


def get_orders_status_chart():
    statuses = (
        OrderStatus.objects
        .annotate(
            orders_count=Count(
                "order",
                filter=Q(order__is_paid=True)
            )
        )
        .order_by("id")
    )

    max_count = max(
        [s.orders_count for s in statuses],
        default=1
    )

    return {
        "statuses": statuses,
        "max_count": max_count,
    }


def get_orders_month_count():

    today = timezone.localdate()

    j_today = jdatetime.date.fromgregorian(date=today)

    first_j = jdatetime.date(j_today.year, j_today.month, 1)
    first_day = first_j.togregorian()


    if j_today.month == 12:
        next_j = jdatetime.date(j_today.year + 1, 1, 1)
    else:
        next_j = jdatetime.date(j_today.year, j_today.month + 1, 1)

    next_month = next_j.togregorian()


    days = []
    total_orders = 0
    max_orders = 1

    current = first_day

    while current < next_month:

        start = timezone.make_aware(
            datetime.combine(current, time.min)
        )

        end = timezone.make_aware(
            datetime.combine(current, time.max)
        )


        count = Order.objects.filter(
            is_paid=True,
            payment_date__range=(start, end)
        ).count()


        total_orders += count
        max_orders = max(max_orders, count)


        days.append({
            "day": current,
            "orders": count
        })


        current += timedelta(days=1)


    return {
        "days": days,
        "max_orders": max_orders,
        "total_orders": total_orders,
    }