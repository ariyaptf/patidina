import ephem
import glob
import math
import os
import pylunar

from skyfield.api import load, Topos
from skyfield.trigonometry import position_angle_of

from datetime import datetime, timedelta
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

from django.conf import settings

if settings.DEBUG:
    BASE_DIR = os.path.dirname(__file__)
else:
    BASE_DIR = settings.BASE_DIR


def calculate_moon_phase(date_str=None, before_date_str=None, after_date_str=None):
    # กำหนดค่าคงที่สำหรับพาธ
    moonpath = os.path.join(BASE_DIR, 'static/utils/moon/moon.png')

    # ตรวจสอบและตั้งค่าวันที่
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        date = datetime.now()

    # คำนวณวันที่ก่อนหน้าและหลังจากตามที่ระบุ
    before_days = int(before_date_str) if before_date_str else 0
    after_days = int(after_date_str) if after_date_str else 0

    # คำนวณช่วงเวลา
    start_date = date - timedelta(days=before_days)
    end_date = date + timedelta(days=after_days)

    # ลบไฟล์ทั้งหมดในโฟลเดอร์ ยกเว้น 'moon.png'
    delete_files_except(os.path.dirname(moonpath), 'moon.png')

    # วนลูปคำนวณและสร้างภาพเงาดวงจันทร์ในช่วงเวลานี้
    current_date = start_date
    while current_date <= end_date:
        calculate_and_draw_moon_phase_for_date(current_date, moonpath)
        current_date += timedelta(days=1)


def calculate_and_draw_moon_phase_for_date(date, moonpath):
    observer = ephem.Observer()
    observer.date = date

    # สร้างชื่อไฟล์ตามวันที่
    filename = date.strftime('%Y-%m-%d.png')
    phasepath = os.path.join(BASE_DIR, f'static/utils/moon/{filename}')

    m = ephem.Moon(observer)
    m.compute(observer)
    a = m.elong
    phase = m.moon_phase
    phase = 1 - phase
    if a > 0:
        phase = -phase

    draw_moon_phase(moonpath, phasepath, phase)


def decimal_to_deg_min_sec(decimal_value):
    degrees = int(decimal_value)
    minutes_with_decimal = (decimal_value - degrees) * 60
    minutes = int(minutes_with_decimal)
    seconds = (minutes_with_decimal - minutes) * 60
    return degrees, minutes, seconds


def delete_files_except(directory, except_file):
    for file in glob.glob(os.path.join(directory, '*')):
        if not file.endswith(except_file):
            os.remove(file)


def draw_moon_phase(moonpath, phasepath, phase):
    with Image(filename=moonpath) as img:
        radius = img.height // 2
        with Drawing() as draw:
            draw.fill_color = Color("rgba(0, 0, 0, 0.7)")
            if phase < 0:
                phase = abs(phase)
                for y in range(radius):
                    x = math.sqrt(radius**2 - y**2)
                    x = round(x)
                    X = radius - x
                    Y = radius - y
                    Y_mirror = radius + y
                    moon_width = 2 * (radius - X)
                    shade = moon_width * phase
                    shade = round(shade)
                    x_shade = X + shade
                    draw.line((X, Y), (x_shade, Y))
                    if Y_mirror != Y:
                        draw.line((X, Y_mirror), (x_shade, Y_mirror))
                draw(img)
                img.save(filename=phasepath)

            elif phase > 0:
                phase = abs(phase)
                for y in range(radius):
                    x = math.sqrt(radius**2 - y**2)
                    x = round(x)
                    X = radius + x
                    Y = radius - y
                    Y_mirror = radius + y
                    moon_width = 2 * (radius - X)
                    shade = moon_width * phase
                    shade = round(shade)
                    x_shade = X + shade
                    draw.line((X, Y), (x_shade, Y))
                    if Y_mirror != Y:
                        draw.line((X, Y_mirror), (x_shade, Y_mirror))
                draw(img)
                img.save(filename=phasepath)


def next_full_moon(date_str=None):
    # ตรวจสอบและตั้งค่าวันที่
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    else:
        date = datetime.now()

    observer = ephem.Observer()
    observer.date = date
    dt = ephem.next_full_moon(observer.date)
    dtlocal = ephem.localtime(dt)
    fullmoon = dtlocal.strftime('%Y-%m-%d')

    return fullmoon

