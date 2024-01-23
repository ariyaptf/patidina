import http.client
import requests
import json
import calendar
from django.views import View
from django.shortcuts import render
from datetime import date, datetime, timedelta
from django.http import (
    Http404,
    HttpResponse,
    JsonResponse,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import EventIndexPage
from utils.models import (
    ImportantDaysInLunarCalendar,
    ImportantDaysInSolarCalendar,
    UposathaOfPakkhaganana
)
from utils.calendar import (
    adhikamasa,
    th_lunar_date,
    collect_uposatha_date,
    adhikamasa
)


def events_api(request):
    # รับพารามิเตอร์ 'start' และ 'end' จากคำขอ
    start_param = request.GET.get('start', '')
    end_param = request.GET.get('end', '')

    # คำนวณวันแรกของเดือนปัจจุบัน
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)

    # คำนวณวันสุดท้ายของเดือนปัจจุบัน
    last_day_of_month = date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

    # ตั้งค่าวันที่เริ่มต้นและสิ้นสุด
    start_date = datetime.fromisoformat(start_param) if start_param else first_day_of_month
    end_date = datetime.fromisoformat(end_param) if end_param else last_day_of_month
    adhikamasa_year = adhikamasa(start_date.year)
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    uposatha_dates  = collect_uposatha_date(dates)

    # ขั้นตอนที่ 1 แสดงปฏิทินจันทรคติ
    # วนลูปจาก start_date ถึง end_date
    current_date = start_date
    event_data = []

    for i in range((end_date - start_date).days + 1):
        day_date = start_date + timedelta(days=i)
        lunar_date = th_lunar_date(day_date)
        if any(lunar_date == uposatha_date['ld'] for uposatha_date in uposatha_dates):
            phase = ' '.join(lunar_date.split()[:2])
            if phase == 'ขึ้น 15':
                title = '🌕' + lunar_date
            elif phase == 'แรม 8':
                title = '🌗' + lunar_date
            elif phase == 'แรม 14':
                title = '🌑' + lunar_date
            elif phase == 'แรม 15':
                title = '🌑' + lunar_date
            elif phase == 'ขึ้น 8':
                title = '🌓' + lunar_date
            else:
                title = lunar_date

            event_data.append({
                "title": title,
                "start": day_date.isoformat(),  # แปลงเป็นสตริง ISO
                "groupId": "uposatha_date",
            })

        else:
            # ถ้าไม่ตรงกัน, เพิ่มเหตุการณ์ปกติ
            event_data.append({
                "title": lunar_date,
                "start": day_date.isoformat(),
                "groupId": "th_lunar_date",
            })

    # ดึงข้อมูลเหตุการณ์ตามช่วงวันที่จาก UposathaOfPakkhaganana
    dmy_obs = UposathaOfPakkhaganana.objects.filter(
        selected_date__gte=start_date,
        selected_date__lte=end_date
    )

    # ขั้นตอนที่ 2 วันพระตามธรรมยุต
    for event in dmy_obs:
        start_iso = datetime.combine(event.selected_date, datetime.min.time()).isoformat()
        date_object = datetime.strptime(start_iso, '%Y-%m-%dT%H:%M:%S')
        lunar_date = th_lunar_date(date_object)
        title = ''
        if any(lunar_date == uposatha_date['ld'] for uposatha_date in uposatha_dates):
            pass
        else:
            phase = ' '.join(lunar_date.split()[:2])
            if phase not in ['ขึ้น 15', 'แรม 8', 'แรม 14', 'แรม 15', 'ขึ้น 8']:
                if event.moon_phase == 'new_moon':
                    title = '🌑' + 'ธรรมยุต'
                elif event.moon_phase == 'first_quarter':
                    title = '🌓' + 'ธรรมยุต'
                elif event.moon_phase == 'full_moon':
                    title = '🌕' + 'ธรรมยุต'
                elif event.moon_phase == 'last_quarter':
                    title = '🌗' + 'ธรรมยุต'

        event_data.append({
            "title": title,
            "start": start_iso,  # แปลงเป็นสตริง ISO
            "groupId": "uposatha_event",
        })

    # ขั้นตอนที่ 3 วันสำคัญตามปฏิทินจันทรคติ
    lunar_imptdays_data = ImportantDaysInLunarCalendar.objects.all().prefetch_related('lunar_calendar_details')
    lunar_impt_days_dict = {}
    for day in lunar_imptdays_data:
        details_list = [detail.name for detail in day.lunar_calendar_details.all()]
        # จัดเก็บใน dictionary
        if adhikamasa_year:
            lunar_impt_days_dict[day.lunar_date_in_adhikamasa] = {
                'important_day': day,
                'details': details_list
            }
        else:
            lunar_impt_days_dict[day.lunar_date] = {
                'important_day': day,
                'details': details_list
            }

    for i in range((end_date - start_date).days + 1):
        day_date = start_date + timedelta(days=i)
        lunar_date = th_lunar_date(day_date)

        if lunar_date in lunar_impt_days_dict:
            titles = lunar_impt_days_dict[lunar_date]['details']
            for title in titles:
                event_data.append({
                    "title": f"{title}",
                    "start": day_date.isoformat(),  # แปลงเป็นสตริง ISO
                    "groupId": "holiday",
                })

    # ขั้นตอนที่ 4 วันสำคัญตามปฏิทินสุริยคติ
    solar_imptdays_data = ImportantDaysInSolarCalendar.objects.all().prefetch_related('solar_calendar_details')
    solar_impt_days_dict = {}
    for each_day in solar_imptdays_data:
        details_list = [detail.name for detail in each_day.solar_calendar_details.all()]
        # จัดเก็บใน dictionary
        solar_impt_days_dict[f"{each_day.day}-{each_day.month}"] = {
            'details': details_list
        }

    for i in range((end_date - start_date).days + 1):
        day_date = start_date + timedelta(days=i)

        if f"{day_date.day}-{day_date.month}" in solar_impt_days_dict:
            titles = solar_impt_days_dict[f"{day_date.day}-{day_date.month}"]['details']
            for title in titles:
                event_data.append({
                    "title": f"{title}",
                    "start": day_date.isoformat(),  # แปลงเป็นสตริง ISO
                    "groupId": "holiday",
                })

    return JsonResponse(event_data, safe=False)


def today_message_get_calendar_events(request):
    """
    JSON list of events compatible with fullcalendar.js
    """
    # Parse input.
    try:
        page_id = request.GET["pid"]
    except KeyError:
        return HttpResponse("pid required", status=400)

    start = None
    end = None
    start_str = request.GET.get("start", None)
    end_str = request.GET.get("end", None)
    try:
        if start_str:
            start = timezone.make_aware(
                datetime.strptime(start_str[:10], "%Y-%m-%d"),
            )
        if end_str:
            end = timezone.make_aware(
                datetime.strptime(end_str[:10], "%Y-%m-%d"),
            )
    except ValueError:
        return HttpResponse(
            "start and end must be valid datetimes.", status=400
        )

    # Get the page.
    try:
        page = EventIndexPage.objects.get(pk=page_id).specific
    except (EventIndexPage.DoesNotExist, ValueError):
        raise Http404("Page does not exist")

    return JsonResponse(
        page.get_calendar_events(start=start, end=end), safe=False
    )



class TestSms(View):
    def get(self, request):
        conn = http.client.HTTPSConnection("n81245.api.infobip.com")
        payload = json.dumps({
            "messages": [
                {
                    "destinations": [{"to":"66984265365"},{"to":"66984265365"}],
                    "from": "ServiceSMS",
                    "text": "Hello,\n\nThis is a test message from Infobip. Have a nice day!"
                }
            ]
        })
        headers = {
            'Authorization': 'App f29fbe087889e72069c8d63db2c63389-1244cce2-43d8-409b-88e0-112e5674e0b7',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        conn.request("POST", "/sms/2/text/advanced", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

        return render(request, "website/pages/test_sms.html", {
            "data": data,
        })



def send_otp(request):
    # ตรวจสอบว่าเป็นการคำขอ POST และมีข้อมูลเบอร์โทรศัพท์
    if request.method == 'POST' and 'phone_number' in request.POST:
        phone_number = request.POST['phone_number']
        api_key = 'f29fbe087889e72069c8d63db2c63389-1244cce2-43d8-409b-88e0-112e5674e0b7'  # ใส่ API Key ของคุณที่นี่
        infobip_url = 'https://n81245.api.infobip.com'

        headers = {
            'Authorization': f'App {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        # สร้างข้อความ OTP ของคุณ (แนะนำให้สร้างข้อความแบบสุ่ม)
        otp_message = 'Your OTP is: 1234'

        data = {
            'from': 'InfoSMS',
            'to': phone_number,
            'text': otp_message
        }

        # ส่งคำขอไปยัง Infobip
        response = requests.post(infobip_url, headers=headers, json=data)

        # ตรวจสอบสถานะการตอบกลับ
        if response.status_code == 200:
            return JsonResponse({'message': 'OTP sent successfully!'})
        else:
            return JsonResponse({'error': 'Failed to send OTP'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def show_otp_form(request):
    # เพียงเรนเดอร์ฟอร์มที่อยู่ใน template 'otp_form.html'
    return render(request, 'website/pages/otp_form.html')
