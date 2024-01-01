import calendar
import re
import math
from astropy.time import Time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import ephem
from pylunar import MoonInfo
from pythaidate import CsDate

# 1. xl_mod Function
def xl_mod(a, b):
    """
    คืนค่าผลลัพธ์ของการดำเนินการ modulo ระหว่างสองตัวเลข.

    ฟังก์ชันนี้คืนค่าผลลัพธ์ของ 'a % b', ซึ่งเป็นเศษที่เหลือจากการหาร 'a' ด้วย 'b'.
    สามารถใช้สำหรับการคำนวณทางคณิตศาสตร์ที่ต้องการหาค่าเศษจากการหาร.

    Parameters:
    a (float or int): ตัวตั้งในการดำเนินการหาร.
    b (float or int): ตัวหาร.

    Returns:
    float or int: ค่าเศษที่เหลือจากการหาร 'a' ด้วย 'b'.

    ตัวอย่าง:
    >>> xl_mod(10, 3)
    1
    >>> xl_mod(5.5, 2.1)
    1.3
    """
    return a % b


# 2. adhikamasa Function
def adhikamasa(iYear):
    """
    ตรวจสอบว่าปีที่ระบุเป็นปีอธิกมาสหรือไม่.

    ปีอธิกมาสในปฏิทินจันทรคติไทยเป็นปีที่มีจำนวนวันมากกว่าปกติ เนื่องจากการเพิ่มขึ้นของจำนวนวันในเดือนบางเดือน.
    ฟังก์ชันนี้จะคำนวณว่าปีที่ระบุอยู่ภายใต้เงื่อนไขปีอธิกมาสหรือไม่ โดยอิงจากสูตรคำนวณที่กำหนดไว้.

    Parameters:
    iYear (int): ปี ค.ศ. ที่ต้องการตรวจสอบ.

    Returns:
    bool: ค่าบูลีนที่แสดงว่าปีที่ระบุเป็นปีอธิกมาสหรือไม่.

    ตัวอย่าง:
    >>> adhikamasa(2023)
    True
    >>> adhikamasa(2024)
    False
    """
    Athi = xl_mod((iYear - 78) - 0.45222, 2.7118886)
    return Athi < 1


# 6. athikasurathin Function
def athikasurathin(iYear):
    """
    ตรวจสอบว่าปีที่ระบุเป็นปีอธิกสุรทินหรือไม่.

    ปีอธิกสุรทินเป็นปีที่มีวันที่ 29 กุมภาพันธ์ ซึ่งเกิดขึ้นทุกๆ 4 ปี แต่ยกเว้นปีที่หารด้วย 100 ได้ลงตัว
    แต่ไม่หารด้วย 400 ได้ลงตัว ฟังก์ชันนี้จะคืนค่า True หากเป็นปีอธิกสุรทิน และ False ถ้าไม่ใช่.

    Parameters:
    iYear (int): ปีที่ต้องการตรวจสอบ.

    Returns:
    bool: ค่าบูลีนที่แสดงว่าปีที่ระบุเป็นปีอธิกสุรทินหรือไม่.

    ตัวอย่าง:
    >>> athikasurathin(2000)
    True
    >>> athikasurathin(1900)
    False
    >>> athikasurathin(2024)
    True
    """

    if iYear % 400 == 0:
        return True
    elif iYear % 100 == 0:
        return False
    elif iYear % 4 == 0:
        return True
    else:
        return False


# 7. the_days_in_a_solar_year Function
# สำหรับแสดงจำนวนวันใน 1 ปีตามแบบสุริยคติ
def the_days_in_a_solar_year(input_date):
    """
    คำนวณจำนวนวันในปีสุริยคติสำหรับปีที่ระบุ.

    ฟังก์ชันนี้จะตรวจสอบว่าปีของวันที่ที่ระบุเป็นปีอธิกสุรทินหรือไม่ (ปีที่มี 366 วัน)
    และคืนค่าจำนวนวันทั้งหมดในปีนั้น. ปีอธิกสุรทินเป็นปีที่มีวันที่ 29 กุมภาพันธ์.

    Parameters:
    input_date (datetime.date): วันที่ที่ต้องการคำนวณจำนวนวันในปีสุริยคติ.

    Returns:
    int: จำนวนวันในปีสุริยคติของปีที่ระบุ (365 หรือ 366 วัน).

    ตัวอย่าง:
    >>> the_days_in_a_solar_year(datetime.date(2024, 1, 1))
    366
    >>> the_days_in_a_solar_year(datetime.date(2023, 1, 1))
    365
    """
    return 366 if athikasurathin(input_date.year) else 365


# 8. thai_to_arabic
# แปลงเลขไทยเป็นอาราบิค
def thai_to_arabic(thai_number):
    thai_to_arabic_digits = {
        '๐': '0',
        '๑': '1',
        '๒': '2',
        '๓': '3',
        '๔': '4',
        '๕': '5',
        '๖': '6',
        '๗': '7',
        '๘': '8',
        '๙': '9'
    }

    arabic_number = ''.join(thai_to_arabic_digits.get(digit, digit) for digit in thai_number)
    return arabic_number


# 9. th_lunar_date Function
def th_lunar_date(input_date):
    # แปลง คริสตศักราช เป็น JDN
    t = Time(input_date.strftime('%Y-%m-%d'))
    cs = CsDate.fromjulianday(math.ceil(t.jd))
    parts = cs.csformat().split(' ')
    return f"{parts[3]} {thai_to_arabic(parts[4]).strip()} {parts[5]} {parts[1]} {thai_to_arabic(parts[2]).strip()}"


# 10. find_thai_newyear_lunar_date Function
def find_thai_newyear_lunar_date(year):
    """
    ค้นหาวันที่ของวันปีใหม่ไทยตามปฏิทินจันทรคติในปีที่กำหนด.

    ฟังก์ชันนี้จะวนซ้ำผ่านทุกวันในปีที่ระบุเพื่อหาวันที่ที่ตรงกับ 'ขึ้น 1 ค่ำ เดือน 5' ตามปฏิทินจันทรคติไทย,
    ซึ่งถือเป็นวันปีใหม่ไทย. หากพบวันที่นั้น, ฟังก์ชันจะคืนค่าวันที่นั้น. หากไม่พบ, จะคืนค่า 0.

    Parameters:
    year (int): ปีที่ต้องการค้นหาวันปีใหม่ไทย.

    Returns:
    datetime.date: วันที่ของวันปีใหม่ไทยตามปฏิทินจันทรคติหรือคืนค่า 0 หากไม่พบ.

    ตัวอย่าง:
    >>> find_thai_newyear_lunar_date(2023)
    datetime.date(2023, 4, 14)
    """
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    current_date = start_date
    while current_date < end_date:
        result = th_lunar_date(current_date)
        if result == 'ขึ้น 1 ค่ำ เดือน 5':
            return current_date
        current_date += timedelta(days=1)

    return 0


# 11. th_zodiac Function
def th_zodiac(input_date, output_type=1):
    zodiac_animals = {
        1: ["ปีชวด", "ปีฉลู", "ปีขาล", "ปีเถาะ", "ปีมะโรง", "ปีมะเส็ง", "ปีมะเมีย", "ปีมะแม", "ปีวอก", "ปีระกา", "ปีจอ", "ปีกุน"],
        2: ["RAT", "OX", "TIGER", "RABBIT", "DRAGON", "SNAKE", "HORSE", "GOAT", "MONKEY", "ROOSTER", "DOG", "PIG"],
        3: list(range(1, 13))
    }
    # แปลง คริสตศักราช เป็นจุลศักราช
    year = era(input_date, 10)
    cs=CsDate(int(year), input_date.month, input_date.day)
    parts = cs.csformat().split(' ')
    result = f"{parts[6]}"
    position = zodiac_animals[1].index(result)

    return zodiac_animals[output_type][position]


# 12. convert_thnum Function
def convert_thnum(strInput):
    """
    แปลงตัวเลขอารบิก (0-9) ในสตริงที่ระบุเป็นตัวเลขไทย (๐-๙).

    ฟังก์ชันนี้จะทำการแสกนสตริงที่รับเข้ามา และแปลงทุกตัวเลขอารบิกที่ปรากฏในสตริงเป็นรูปแบบของตัวเลขไทยที่สอดคล้องกัน.

    Parameters:
    strInput (str): สตริงที่มีตัวเลขอารบิกที่ต้องการแปลงเป็นตัวเลขไทย.

    Returns:
    str: สตริงที่มีตัวเลขไทยแทนที่ตัวเลขอารบิก.

    ตัวอย่าง:
    >>> convert_thnum("ปี 2023")
    'ปี ๒๐๒๓'
    """
    numberArray = ["0", "๐", "1", "๑", "2", "๒", "3", "๓", "4", "๔", "5", "๕", "6", "๖", "7", "๗", "8", "๘", "9", "๙"]
    for i in range(0, len(numberArray), 2):
        strInput = strInput.replace(numberArray[i], numberArray[i + 1])
    return strInput


# 13. th_lunar_holiday Function
def th_lunar_holiday(input_date):
    """
    คืนค่าชื่อวันหยุดตามปฏิทินจันทรคติไทยสำหรับวันที่กำหนด.

    ฟังก์ชันนี้จะตรวจสอบวันที่ตามปฏิทินจันทรคติไทยและคืนค่าชื่อของวันหยุดพิเศษ หากวันที่นั้นเป็นวันหยุด.
    รายการวันหยุดจะแตกต่างกันไปในปีที่มี 'อธิกมาส' หรือเดือนที่เพิ่มเติมตามปฏิทินจันทรคติ.

    Parameters:
    input_date (datetime.date): วันที่ที่ต้องการตรวจสอบวันหยุด.

    Returns:
    str: ชื่อของวันหยุดในปฏิทินจันทรคติไทยสำหรับวันที่ที่กำหนด หากไม่มีวันหยุดในวันนั้น จะคืนค่าเป็นสตริงว่าง.

    ตัวอย่าง:
    >>> th_lunar_holiday(datetime.date(2023, 5, 6))
    'วันวิสาขบูชา'

    หมายเหตุ:
    ฟังก์ชันนี้สมมติว่ามีฟังก์ชัน 'th_lunar_date' ที่คืนค่าวันที่ตามปฏิทินจันทรคติไทยเป็นสตริง
    ตัวอย่างเช่น "ขึ้น 15 ค่ำ เดือน 3".
    """
    if adhikamasa(input_date.year):
        special_dates = {
            "แรม 15 ค่ำ เดือน 2": "วันพระอัครสาวกบรรพชา",
            "ขึ้น 7 ค่ำ เดือน 3": "วันพระโมคคัลานะสำเร็จเป็นพระอรหันต์",
            "ขึ้น 15 ค่ำ เดือน 4": "วันมาฆบูชา, วันพระสารีบุตรสำเร็จเป็นพระอรหันต์",
            "แรม 5 ค่ำ เดือน 4": "วันเสร็จสิ้นการปฐมสังคานา",
            "แรม 1 ค่ำ เดือน 6": "วันเสร็จโปรดพระประยูรญาติ",
            "แรม 6 ค่ำ เดือน 6": "วันพระราหุลบรรพชา",
            "ขึ้น 15 ค่ำ เดือน 7": "วันวิสาขบูชา",
            "แรม 8 ค่ำ เดือน 7": "วันอัฏฐมีบูชา",
            "แรม 5 ค่ำ เดือน 8": "วันพระปัญจวัคคีย์สำเร็จเป็นพระอรหันต์",
            "ขึ้น 15 ค่ำ เดือน 88": "วันอาสาฬหบูชา",
            "แรม 1 ค่ำ เดือน 88": "วันเข้าพรรษาแรก (ปุริมพรรษา)",
            "แรม 1 ค่ำ เดือน 9": "วันเข้าพรรษาหลัง (ปัจฉิมพรรษา)",
            "แรม 4 ค่ำ เดือน 9": "วันพระอานนท์สำเร็จเป็นพระอรหันต์",
            "แรม 5 ค่ำ เดือน 9": "วันปฐมสังคายนา",
            "แรม 5 ค่ำ เดือน 10": "วันสารทไทย",
            "ขึ้น 15 ค่ำ เดือน 11": "วันออกพรรษาแรก (ปุริมพรรษา)",
            "ขึ้น 15 ค่ำ เดือน 12": "วันพระสาริบุตรปรินิพพาน, วันออกพรรษาหลัง (ปัจฉิมพรรษา), วันลอยกระทง",
            "แรม 15 ค่ำ เดือน 12": "วันพระโมคคัลานะปรินิพพาน"
        }
    else:
        special_dates = {
            "แรม 15 ค่ำ เดือน 2": "วันพระอัครสาวกบรรพชา",
            "ขึ้น 7 ค่ำ เดือน 3": "วันพระโมคคัลานะสำเร็จเป็นพระอรหันต์",
            "ขึ้น 15 ค่ำ เดือน 3": "วันมาฆบูชา, วันพระสารีบุตรสำเร็จเป็นพระอรหันต์",
            "แรม 5 ค่ำ เดือน 4": "วันเสร็จสิ้นการปฐมสังคานา",
            "แรม 1 ค่ำ เดือน 6": "วันเสร็จโปรดพระประยูรญาติ",
            "แรม 6 ค่ำ เดือน 6": "วันพระราหุลบรรพชา",
            "ขึ้น 15 ค่ำ เดือน 6": "วันวิสาขบูชา",
            "แรม 8 ค่ำ เดือน 6": "วันอัฏฐมีบูชา",
            "แรม 5 ค่ำ เดือน 8": "วันพระปัญจวัคคีย์สำเร็จเป็นพระอรหันต์",
            "ขึ้น 15 ค่ำ เดือน 8": "วันอาสาฬหบูชา",
            "แรม 1 ค่ำ เดือน 8": "วันเข้าพรรษาแรก (ปุริมพรรษา)",
            "แรม 1 ค่ำ เดือน 9": "วันเข้าพรรษาหลัง (ปัจฉิมพรรษา)",
            "แรม 4 ค่ำ เดือน 9": "วันพระอานนท์สำเร็จเป็นพระอรหันต์",
            "แรม 5 ค่ำ เดือน 9": "วันปฐมสังคายนา",
            "แรม 5 ค่ำ เดือน 10": "วันสารทไทย",
            "ขึ้น 15 ค่ำ เดือน 11": "วันออกพรรษาแรก (ปุริมพรรษา)",
            "ขึ้น 15 ค่ำ เดือน 12": "วันพระสาริบุตรปรินิพพาน, วันออกพรรษาหลัง (ปัจฉิมพรรษา), วันลอยกระทง",
            "แรม 15 ค่ำ เดือน 12": "วันพระโมคคัลานะปรินิพพาน"
        }

    lunar_date = th_lunar_date(input_date)

    # Assuming th_lunar_date returns a string like "ขึ้น 15 ค่ำ เดือน 3"
    return special_dates.get(lunar_date, "")


# 14. era Function
def era(input_date, output_type=1):
    """
    แปลงวันที่ที่กำหนดให้เป็นรูปแบบศักราชต่างๆ ตามประเภทที่กำหนด.

    Parameters:
    input_date (datetime.date): วันที่ที่จะแปลง.
    output_type (int, optional): ประเภทของศักราชที่ต้องการ. ค่าเริ่มต้นคือ 1.
                                1 สำหรับพุทธศักราช,
                                2 สำหรับจุลศักราช,
                                3 สำหรับมหาศักราช,
                                4 สำหรับรัตนโกสินทร์ศก,
                                5 สำหรับคริสตศักราช.

    Returns:
    str: สตริงที่แสดงวันที่ในรูปแบบศักราชที่เลือก.

    ตัวอย่าง:
    >>> era(datetime.date(2023, 1, 1), 1)
    'พุทธศักราช 2566'

    >>> era(datetime.date(2023, 1, 1), 5)
    'คริสตศักราช 2023'
    """

    if output_type == 1:
        return "พุทธศักราช " + str(input_date.year + 543)
    elif output_type == 2:
        return "จุลศักราช " + str(input_date.year - 638)
    elif output_type == 3:
        return "มหาศักราช " + str(input_date.year - 78)
    elif output_type == 4:
        return "รัตนโกสินทร์ศก " + str(input_date.year - 1781)
    elif output_type == 5:
        return "คริสตศักราช " + str(input_date.year)
    elif output_type == 6:
        return "พ.ศ. " + str(input_date.year + 543)
    elif output_type == 7:
        return "ค.ศ. " + str(input_date.year)
    elif output_type == 8: # 2567 (พ.ศ.)
        return str(input_date.year + 543)
    elif output_type == 9: # 2024 (ค.ศ.)
        return str(input_date.year)
    elif output_type == 10: # จ.ศ.
        return str(input_date.year - 638)
    elif output_type == 11: # 67 (พ.ศ.)
        return str(input_date.year + 543)[2:]
    else:
        return ""


# 15 get uposatha date
def get_uposatha_date(given_date=datetime.now(), months_to_calculate=2):
    uposatha_dates = []

    for month in range(months_to_calculate):
        # คำนวณวันที่สำหรับเดือนที่กำหนด
        month_date = (given_date + relativedelta(months=month)).replace(day=1)
        last_day_of_month = calendar.monthrange(month_date.year, month_date.month)[1]
        solar_dates = [date(month_date.year, month_date.month, day) for day in range(1, last_day_of_month + 1)]

        # เพิ่มการตรวจสอบการซ้ำกันของวันที่ก่อนเพิ่มลงใน uposatha_dates
        for uposatha_date in collect_uposatha_date(solar_dates):
            if uposatha_date not in uposatha_dates:
                uposatha_dates.append(uposatha_date)

    return uposatha_dates


# 15.1 use with get_uposatha_date
def collect_uposatha_date(dates):
    result = []

    for solar_date in dates:
        lunar_date = th_lunar_date(solar_date)
        lunar_no, lunar_month = lunar_date.split(" ")[1], lunar_date.split(" ")[3]
        lunar_phase = lunar_date.split(" ")[0]
        if lunar_no in ['8', '14', '15']:
            if not (lunar_no == '14' and lunar_phase == "ขึ้น"):
                result.append({'ld': lunar_date, 'sd': solar_date, 'month': lunar_month})

    # สร้างรายการเพื่อเก็บวันที่ 'แรม 15 ค่ำ'
    dates_with_15 = {d['sd'] for d in result if "แรม 15 ค่ำ" in d['ld']}

    # ลบ 'แรม 14 ค่ำ' ออกหากมี 'แรม 15 ค่ำ' ในเดือนเดียวกัน
    result_final = []
    for date in result:
        if "แรม 14 ค่ำ" in date['ld']:
            # ตรวจสอบว่ามี 'แรม 15 ค่ำ' ในเดือนเดียวกันหรือไม่
            next_month = (date['sd'].replace(day=28) + timedelta(days=4)).replace(day=1)
            if any(d >= date['sd'] and d < next_month for d in dates_with_15):
                continue
        result_final.append(date)

    return result_final









# 16 next_4_phase
def next_4_phase(given_date=datetime.now(), latitude=(13, 45, 23), longitude=(100, 30, 7)):
    # สร้างอ็อบเจ็กต์ MoonInfo
    mi = MoonInfo(latitude, longitude)

    # ตั้งค่าวันที่และเวลาให้กับ MoonInfo
    mi.update((given_date.year, given_date.month, given_date.day, 0, 0, 0))

    # หาค่าวันพระจากสถานะสำคัญ 4 สถานะคือ
    result = mi.next_four_phases()

    return result


# 17. is_adhikamasa_year
# ตรวจสอบว่าปีนี้มีเดือน อธิกมาสหรือไม่
def is_adhikamasa_year(input_year):
    """
    Check if the given year is an adhikamasa year in the lunar calendar.

    Args:
    input_year (int): Year to check.

    Returns:
    bool: True if it's an adhikamasa year, False otherwise.
    """
    for month in range(1, 13):
        # Create date object for the 1st day of each month in the given year
        first_day_of_month = date(input_year, month, 1)
        # Convert to Julian day
        t = Time(first_day_of_month.strftime('%Y-%m-%d'))
        # Convert to CsDate
        cs = CsDate.fromjulianday(math.ceil(t.jd))
        # Check for leap month
        if cs.leap_month:
            return True

    return False


