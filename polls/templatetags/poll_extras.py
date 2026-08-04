from django import template
import jdatetime
from django.utils.safestring import mark_safe

from order_module.models import PostingMethod

register = template.Library()

@register.filter(name='show_jalali_date')
def show_jalali_date(value):
    if value:
        jalali_date = jdatetime.datetime.fromgregorian(datetime=value)
        return jalali_date.strftime('%Y/%m/%d')
    return ''

@register.filter(name='three_digits_currency')
def three_digits_currency(value):
    value = '{:,}'.format(value)

    persian = '۰۱۲۳۴۵۶۷۸۹'
    english = '0123456789'

    value = value.translate(
        str.maketrans(english, persian)
    )

    return value + ' تومان'

@register.filter(name='three_digits_currency_no_extension')
def three_digits_currency(value):
    value = '{:,}'.format(value)

    persian = '۰۱۲۳۴۵۶۷۸۹'
    english = '0123456789'

    value = value.translate(
        str.maketrans(english, persian)
    )

    return value

@register.filter(name='three_digits_currency_rials')
def three_digits_currency_rials(value):
    value = '{:,}'.format(value)

    persian = '۰۱۲۳۴۵۶۷۸۹'
    english = '0123456789'

    value = value.translate(
        str.maketrans(english, persian)
    )

    return value + ' ریال'

@register.filter(name='to_fanum')
def fa_num(value):
    return str(value).translate(
        str.maketrans(
            '0123456789',
            '۰۱۲۳۴۵۶۷۸۹'
        )
    )

@register.filter
def in_list(value, my_list):
    return str(value) in my_list

@register.filter
def is_liked(comment, user):
    return comment.like.filter(id=user.id).exists()


@register.filter
def format_card_number(value):
    digits = ''.join(filter(str.isdigit, str(value)))
    groups = [digits[i:i+4] for i in range(0, len(digits), 4)]
    return mark_safe(fa_num('&nbsp;'.join(groups)))


@register.filter
def progress(value):
    if value == 25:
        return value -25
    elif value == 50:
        return value - 15
    elif value == 75:
        return value - 10
    elif value == 100:
        return value

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context["request"].GET.copy()

    for k, v in kwargs.items():
        query[k] = v

    return query.urlencode()


WEEKDAYS = [
    "دوشنبه",
    "سه‌شنبه",
    "چهارشنبه",
    "پنجشنبه",
    "جمعه",
    "شنبه",
    "یکشنبه",
]

@register.filter(name='jalali_weekday')
def weekday_fa(value):
    return WEEKDAYS[value.weekday()]

MONTHS = [
    'فروردین',
    'اردیبهشت',
    'خرداد',
    'تیر',
    'مرداد',
    'شهریور',
    'مهر',
    'آبان',
    'آذر',
    'دی',
    'بهمن',
    'اسفند',
]

@register.filter(name='jalali_month')
def month_fa(value):
    if isinstance(value, int):
        month_number = value
    else:
        month_number = value.month
    return MONTHS[month_number - 1]

@register.filter
def pack_price(price, weight):
    try:
        return int(float(price) * float(weight))
    except (TypeError, ValueError):
        return 0