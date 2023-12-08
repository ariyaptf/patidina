from django import template
import datetime

register = template.Library()

@register.inclusion_tag('website/templatetags/format_lunar_date.html')
def format_lunar_date(lunar_date):
    p = lunar_date.split()
    context = {
        'lunar_phase': p[0],
        'lunar_date': p[1],
        'lunar_date_unit': p[2],
        'lunar_month': p[3] + ' ' + p[4]
    }
    return context


@register.inclusion_tag('website/templatetags/format_solar_date.html')
def format_solar_date(solar_date):
    weekday_name = 'x อาทิตย์ จันทร์ อังคาร พุธ พฤหัสบดี ศุกร์ เสาร์'.split()[solar_date.isoweekday()]
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[solar_date.month]
    context = {
        'solar_dow': weekday_name,
        'solar_date': solar_date.strftime('%-d'),
        'solar_month': month_name
    }
    return context