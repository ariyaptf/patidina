import calendar
import math
from astropy.time import Time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django import template
from django.utils.safestring import mark_safe
from pythaidate import CsDate

from utils.calendar import (
    get_uposatha_date,
    era, th_lunar_date,
    adhikamasa
)
from utils.models import (
    UposathaOfPakkhaganana,
    ImportantDaysInLunarCalendar,
    ImportantDaysInSolarCalendar
)

register = template.Library()


@register.inclusion_tag('website/templatetags/format_lunar_date.html')
def format_lunar_date(lunar_date, BE):
    p = lunar_date.split()
    context = {
        'lunar_phase': p[0],
        'lunar_date': p[1],
        'lunar_date_unit': p[2],
        'lunar_month': p[3] + ' ' + p[4],
        'BE': BE
    }
    return context


@register.inclusion_tag('website/templatetags/format_solar_date.html')
def format_solar_date(solar_date, CE):
    weekday_name = 'x อาทิตย์ จันทร์ อังคาร พุธ พฤหัสบดี ศุกร์ เสาร์'.split()[solar_date.isoweekday()]
    month_name = 'x มกราคม กุมภาพันธ์ มีนาคม เมษายน พฤษภาคม มิถุนายน กรกฎาคม สิงหาคม กันยายน ตุลาคม พฤศจิกายน ธันวาคม'.split()[solar_date.month]
    # แก้ปัญหาบน Windows ปกติเราสามารถใช้ 'solar_date': solar_date.strftime('%d') เพื่อลบ 0 padding
    solar_date = solar_date.strftime('%d')
    if solar_date.startswith('0'):
        solar_date = solar_date[1:]

    context = {
        'solar_dow': weekday_name,
        'solar_date': solar_date,
        'solar_month': month_name,
        'CE': CE
    }
    return context


@register.inclusion_tag('website/templatetags/uposatha_date.html')
def uposatha_date(solar_date, th_zodiac_no, th_zodiac):
    result_of_get_uposatha = get_uposatha_date(solar_date)

    # กรองรายการวันอุโบสถที่มากกว่าหรือเท่ากับวันที่กำหนด
    uposatha_dates = [date for date in result_of_get_uposatha if date['sd'] > solar_date]

    context = {
        'uposatha_1': uposatha_dates[0],
        'uposatha_2': uposatha_dates[1],
        'uposatha_3': uposatha_dates[2],
        'uposatha_4': uposatha_dates[3],
        'moon_1': uposatha_dates[0]['sd'].strftime('%Y-%m-%d.png'),
        'moon_2': uposatha_dates[1]['sd'].strftime('%Y-%m-%d.png'),
        'moon_3': uposatha_dates[2]['sd'].strftime('%Y-%m-%d.png'),
        'moon_4': uposatha_dates[3]['sd'].strftime('%Y-%m-%d.png'),
        'th_zodiac_no': th_zodiac_no,
        'th_zodiac': th_zodiac,
    }
    return context


def get_pakkhaganana_uposatha(solar_date, months_to_calculate):
    # ตั้งค่าวันเริ่มต้นของการกรองเป็นวันที่ 1 ของเดือนปัจจุบัน
    start_date = solar_date.replace(day=1)

    # คำนวณเดือนและปีสำหรับวันสิ้นสุดของการกรอง
    end_date = start_date + relativedelta(months=months_to_calculate, days=-1)

    # กรองข้อมูลในช่วงเวลาที่กำหนด
    upcoming_uposatha = UposathaOfPakkhaganana.objects.filter(selected_date__range=[start_date, end_date])
    return upcoming_uposatha


@register.inclusion_tag('website/templatetags/upcoming_uposatha_dates.html')
def upcoming_uposatha_dates(solar_date, months_to_calculate):
    # จันทรคติ
    uposatha_dates = get_uposatha_date(solar_date, months_to_calculate)

    # วันพระธรรมยุติ
    dmy_uposatha_dates = get_pakkhaganana_uposatha(solar_date, months_to_calculate)

    def get_weekday(date):
        weekdays = ["จ.", "อ.", "พ.", "พฤ.", "ศ.", "ส.", "อา."]
        return weekdays[date.weekday()]

    def find_nearest_date(uposatha_date, dmy_uposatha_dates):
        # แปลง uposatha_date เป็น datetime.date ถ้ามันเป็น datetime
        if isinstance(uposatha_date, datetime):
            uposatha_date = uposatha_date.date()

        for dmy_date in dmy_uposatha_dates:
            # คำนวณความแตกต่างของวันที่
            diff = uposatha_date - dmy_date.selected_date
            # ตรวจสอบความแตกต่างเท่ากับ 1 วันหรือ -1 วัน
            if diff in [timedelta(days=1), timedelta(days=-1)]:
                try:
                    return f"|<span class='text-primary'>{dmy_date.selected_date.strftime('%-d')}</span>"
                except:
                    return f"|<span class='text-primary'>{dmy_date.selected_date.strftime('%#d')}</span>"
        return ''

    # จัดกลุ่มข้อมูลตามเดือน
    monthly_uposatha = defaultdict(list)
    for date in uposatha_dates:
        # หาวันที่ใกล้เคียงใน dmy_uposatha_dates
        nearest_date = find_nearest_date(date['sd'], dmy_uposatha_dates)

        be = era(date['sd'], 11)
        month = f"{ date['sd'].strftime('%m') } { be }"  # แปลงเป็นรูปแบบเดือน ปี
        day = mark_safe(f"{date['sd'].day}{nearest_date}")  # วันที่
        weekday = get_weekday(date['sd'])

        monthly_uposatha[month].append({
            'ld': date['ld'],
            'phase': ' '.join(date['ld'].split()[:2]),
            'day': day,
            'weekday': weekday
        })

    # คำนวณจำนวนช่องว่างที่จำเป็น
    for month, dates in monthly_uposatha.items():
        spaces = 5 - len(dates)  # จำนวนช่องว่างที่จำเป็น
        monthly_uposatha[month].extend([None] * spaces)

    # ส่งข้อมูลนี้ไปยัง Django template
    context = {'monthly_uposatha': dict(monthly_uposatha)}
    return context


@register.filter(name='moonlight_glow')
def moonlight_glow(lunar_date):
    parts = lunar_date.split(" ")
    lunar_phase = parts[0]
    lunar_no = int(parts[1])

    if lunar_phase == 'ขึ้น':
        if lunar_no >= 12:
            return 'fullmoon'
        elif lunar_no >= 8:
            return 'quarter-moon'
    elif lunar_phase == 'แรม':
        if lunar_no <= 4:
            return 'full-moon'
        elif lunar_no <= 8:
            return 'quarter-moon'

    return ''


@register.filter(name='moon_phase')
def moon_phase(lunar_date):
    parts = lunar_date.split(" ")
    lunar_phase = parts[0]
    lunar_no = int(parts[1])

    if lunar_phase == 'ขึ้น':
        if lunar_no == 15:
            return 'เต็ม'
        elif lunar_no == 8:
            return 'กึ่ง'
    elif lunar_phase == 'แรม':
        if lunar_no == 8:
            return 'ลับ'
        elif lunar_no >= 14:
            return 'ดับ'

    return ''


@register.filter(name='next_uposatha_day')
def next_uposatha_day(solar_date):
    # testing
    # solar_date = date(2023,12,13)
    uposatha_dates = get_uposatha_date(solar_date)
    uposatha_days = [date for date in uposatha_dates if date['sd'] >= solar_date]
    next_uposatha = uposatha_days[0]
    difference = (next_uposatha["sd"] - solar_date).days

    if difference == 0:
        return "วันนี้วันพระ"
    elif difference == 1:
        return "พรุ่งนี้วันพระ"
    else:
        return f"อีก {difference} วัน ถึงวันพระ"


@register.filter(name='fraction_format')
def fraction_format(text_with_space_for_split):
    numerator = text_with_space_for_split.split(" ")[0]
    denominator = text_with_space_for_split.split(" ")[1]
    html_content = f"<span><sup>{ numerator }</sup>/<sub>{ denominator }</sub></span>"
    return mark_safe(html_content)


@register.inclusion_tag('website/templatetags/important_day.html')
def important_day(today_solar_date):
    today_lunar_date = th_lunar_date(today_solar_date)
    if adhikamasa(today_solar_date.year):
        lunar_important_days = ImportantDaysInLunarCalendar.objects.filter(
            lunar_date_in_adhikamasa=today_lunar_date
        )
    else:
        lunar_important_days = ImportantDaysInLunarCalendar.objects.filter(
            lunar_date=today_lunar_date
        )

    solar_important_days = ImportantDaysInSolarCalendar.objects.filter(
        day=today_solar_date.day,
        month=today_solar_date.month
    )

    return {
        'lunar_important_days': lunar_important_days,
        'solar_important_days': solar_important_days
    }


@register.inclusion_tag('website/templatetags/organization_info.html')
def organization_info(org_info):
    return {
        'org': org_info
    }
