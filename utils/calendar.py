from datetime import datetime, timedelta

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

# 2. athikamas Function
def athikamas(iYear):
    """
    ตรวจสอบว่าปีที่ระบุเป็นปีอธิกมาสหรือไม่.

    ปีอธิกมาสในปฏิทินจันทรคติไทยเป็นปีที่มีจำนวนวันมากกว่าปกติ เนื่องจากการเพิ่มขึ้นของจำนวนวันในเดือนบางเดือน.
    ฟังก์ชันนี้จะคำนวณว่าปีที่ระบุอยู่ภายใต้เงื่อนไขปีอธิกมาสหรือไม่ โดยอิงจากสูตรคำนวณที่กำหนดไว้.

    Parameters:
    iYear (int): ปี ค.ศ. ที่ต้องการตรวจสอบ.

    Returns:
    bool: ค่าบูลีนที่แสดงว่าปีที่ระบุเป็นปีอธิกมาสหรือไม่.

    ตัวอย่าง:
    >>> athikamas(2023)
    True
    >>> athikamas(2024)
    False
    """
    Athi = xl_mod((iYear - 78) - 0.45222, 2.7118886)
    return Athi < 1

# 3. athikavar Function
def athikavar(iYear):
    """
    ตรวจสอบว่าปีที่ระบุเป็นปีอธิกวารหรือไม่.

    ปีอธิกวารเป็นปีที่มีความคลาดเคลื่อนเฉพาะในการคำนวณปฏิทินจันทรคติไทย โดยขึ้นอยู่กับค่าความคลาดเคลื่อน
    และสถานะของปีอธิกมาสทั้งในปีปัจจุบันและปีถัดไป. ฟังก์ชันนี้จะคืนค่า True หากเป็นปีอธิกวาร
    และ False ถ้าไม่ใช่.

    Parameters:
    iYear (int): ปี ค.ศ. ที่ต้องการตรวจสอบ.

    Returns:
    bool: ค่าบูลีนที่แสดงว่าปีที่ระบุเป็นปีอธิกวารหรือไม่.

    ตัวอย่าง:
    >>> athikavar(2023)
    False
    >>> athikavar(2024)
    True
    """

    if athikamas(iYear):
        return False
    else:
        CutOff = 1.69501433191599E-02 if athikamas(iYear + 1) else -1.42223099315486E-02
        return deviation(iYear) > CutOff

# 4. deviation Function
def deviation(iYear):
    """
    คำนวณค่าความคลาดเคลื่อนสำหรับการตรวจสอบปีอธิกวารจากปี พ.ศ. 2444 ถึง พ.ศ. 3014 (ค.ศ. 1901 ถึง 2471).

    ฟังก์ชันนี้คำนวณค่าความคลาดเคลื่อนสำหรับการตรวจสอบปีอธิกวารโดยอิงจากอาร์เรย์ที่กำหนดไว้ล่วงหน้า.
    ค่านี้ใช้ในการตัดสินว่าปีที่ระบุเป็นปีอธิกวารหรือไม่ โดยอิงจากการคำนวณตามหลักการทางดาราศาสตร์.

    Parameters:
    iYear (int): ปี ค.ศ. ที่ต้องการตรวจสอบ.

    Returns:
    float: ค่าความคลาดเคลื่อนสำหรับปีที่ระบุ หรือ 0 หากปีนั้นไม่อยู่ในช่วงที่รองรับ.

    ตัวอย่าง:
    >>> deviation(1901)
    0.122733000004352
    >>> deviation(2471)
    -0.632191999979482
    """

    # Define StartY array
    StartY = [
        [1901, 0.122733000004352],
        [1906, 1.91890000045229E-02],
        [1911, -8.43549999953059E-02],
        [1916, -0.187898999995135],
        [1921, -0.291442999994964],
        [1926, 7.44250000052413E-02],
        [1931, -2.91189999945876E-02],
        [1936, -0.132662999994416],
        [1941, -0.236206999994245],
        [1946, -0.339750999994074],
        [1951, -0.443294999993903],
        [1956, -7.74269999936981E-02],
        [1961, -0.180970999993527],
        [1966, -0.284514999993356],
        [1971, -0.388058999993185],
        [1976, -0.491602999993014],
        [1981, -0.595146999992842],
        [1986, -0.698690999992671],
        [1991, -0.332822999992466],
        [1996, -0.436366999992295],
        [2001, -0.539910999992124],
        [2006, -0.643454999991953],
        [2011, 0.253001000008218],
        [2016, 0.149457000008389],
        [2021, -0.484674999991406],
        [2026, -0.588218999991235],
        [2031, 0.308237000008937],
        [2036, 0.204693000009108],
        [2041, 0.101149000009279],
        [2046, -2.39499999055015E-03],
        [2051, -0.105938999990379],
        [2056, 0.259929000009826],
        [2061, 0.156385000009997],
        [2066, 5.28410000101682E-02],
        [2071, -5.07029999896607E-02],
        [2076, -0.15424699998949],
        [2081, -0.257790999989318],
        [2086, 0.108077000010887],
        [2091, 4.53300001105772E-03],
        [2096, -9.90109999887712E-02],
        [2101, -0.2025549999886],
        [2106, -0.306098999988429],
        [2111, -0.409642999988258],
        [2116, -4.37749999880528E-02],
        [2121, -0.147318999987882],
        [2126, -0.250862999987711],
        [2131, -0.354406999987539],
        [2136, -0.457950999987368],
        [2141, -0.561494999987197],
        [2146, -0.665038999987026],
        [2151, -0.299170999986821],
        [2156, -0.40271499998665],
        [2161, -0.506258999986479],
        [2166, -0.609802999986308],
        [2171, -0.713346999986137],
        [2176, 0.183109000014035],
        [2181, -0.45102299998576],
        [2186, -0.554566999985589],
        [2191, 0.341889000014582],
        [2196, 0.238345000014753],
        [2201, 0.134801000014924],
        [2206, 3.12570000150951E-02],
        [2211, -7.22869999847338E-02],
        [2216, 0.293581000015471],
        [2221, 0.190037000015642],
        [2226, 8.64930000158135E-02],
        [2231, -1.70509999840154E-02],
        [2236, -0.112095999986102],
        [2241, -0.21563999998593],
        [2246, 9.2094000017526E-02],
        [2251, 2.16499999932857E-02],
        [2256, -6.87919999818992E-02],
        [2261, -0.171263999985486],
        [2266, -0.274807999985315],
        [2271, -0.378351999985144],
        [2276, -0.481895999984973],
        [2281, -0.585439999984802],
        [2286, -0.688983999984631],
        [2291, -0.111115999985743],
        [2296, -0.214659999985571],
        [2301, -0.3182039999854],
        [2306, -0.421747999985229],
        [2311, -0.525291999985058],
        [2316, -0.628835999984887],
        [2321, -0.732379999984716],
        [2326, -0.164750999984511],
        [2331, -0.26829499998434],
        [2336, -0.371838999984169],
        [2341, -0.475382999983998],
        [2346, -0.578926999983827],
        [2351, -0.682470999983656],
        [2356, -8.600699998285E-02],
        [2361, -0.190611999983312],
        [2366, -0.294155999983141],
        [2371, -0.39769999998297],
        [2376, -0.501243999982799],
        [2381, -0.604787999982628],
        [2386, -0.708331999982457],
        [2391, -0.140703999982252],
        [2396, -0.244247999982081],
        [2401, -0.34779199998191],
        [2406, -0.451335999981739],
        [2411, -5.54879999806963E-02],
        [2416, -0.159379999981397],
        [2421, -0.262923999981226],
        [2426, -0.366467999981055],
        [2431, -0.470011999980884],
        [2436, -0.573555999980713],
        [2441, -0.677099999980542],
        [2446, -0.114471999980337],
        [2451, -0.218015999980166],
        [2456, -0.321559999979995],
        [2461, -0.425103999979824],
        [2466, -0.528647999979653],
        [2471, -0.632191999979482],
    ]

    # If iYear is outside the range, return None
    if iYear < 1901 or iYear > 2471:
        return 0

    # Iterate through StartY array and find the corresponding value
    for i in range(len(StartY)):
        if StartY[i][0] == iYear:
            return StartY[i][1]

    # If no match is found, return None
    return 0

# 5. The_days_in_a_lunar_year Function
def The_days_in_a_lunar_year(iYear):
    """
    คำนวณจำนวนวันในปีจันทรคติสำหรับปีที่ระบุ.

    ปีจันทรคติมีจำนวนวันที่แตกต่างกันไปในแต่ละปี ขึ้นอยู่กับว่าเป็นปีอธิกมาสหรือปีอธิกวารหรือไม่.
    ปีอธิกมาสมี 384 วัน ปีอธิกวารมี 355 วัน และปีปกติมี 354 วัน.
    ฟังก์ชันนี้จะคืนค่าจำนวนวันในปีจันทรคติของปีที่ระบุ.

    Parameters:
    iYear (int): ปีจันทรคติที่ต้องการคำนวณจำนวนวัน.

    Returns:
    int: จำนวนวันในปีจันทรคติของปีที่ระบุ (384, 355, หรือ 354 วัน).

    ตัวอย่าง:
    >>> The_days_in_a_lunar_year(2023)
    354
    >>> The_days_in_a_lunar_year(2024)
    384
    """
    if athikamas(iYear):
        return 384
    elif athikavar(iYear):
        return 355
    else:
        return 354

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

# 8 calculate_th_lunar_date Function
def calculate_th_lunar_date(NbLDayYear, RDayPrev, input_date, DayFromOne):
    """
    คำนวณวันที่ตามปฏิทินจันทรคติไทยจากพารามิเตอร์ที่ให้มา.

    ฟังก์ชันนี้จะคำนวณและแปลงวันที่จากปฏิทินสุริยคติไปเป็นปฏิทินจันทรคติไทย 
    โดยอิงจากจำนวนวันในปีจันทรคติ, จำนวนวันที่เหลือในปีก่อนหน้า, วันที่ที่ให้มา, 
    และจำนวนวันตั้งแต่วันที่ 1 มกราคมของปีนั้น.

    Parameters:
    NbLDayYear (int): จำนวนวันในปีจันทรคติ.
    RDayPrev (int): จำนวนวันที่เหลือในปีก่อนหน้า.
    input_date (datetime.date): วันที่ตามปฏิทินสุริยคติที่ต้องการคำนวณ.
    DayFromOne (int): จำนวนวันตั้งแต่วันที่ 1 มกราคมของปีนั้น.

    Returns:
    str: วันที่ตามปฏิทินจันทรคติไทยในรูปแบบสตริง.

    ตัวอย่าง:
    >>> calculate_th_lunar_date(354, 10, datetime.date(2023, 1, 1), 1)
    'ขึ้น 1 ค่ำ เดือน 1'
    """

    ThM, DofY, DofM, ThS, ThZ, ThH, RDayLY = 0, 0, 0, 0, 0, 0, 0
    if NbLDayYear == 354:
        RDayLY = RDayPrev + the_days_in_a_solar_year(input_date)
        DofY = DayFromOne
        
        for j in range(1, 15):
            ThM = j
            
            if j == 1:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 2:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 3:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 4:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 5:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 6:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 7:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 8:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 9:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 10:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 11:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 12:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 13:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 14:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
        
        if ThM > 12:
            ThM = ThM - 12
            ThZ = 1
        else:
            ThZ = 0
        
        if DofY > 15:
            ThS = "แรม "
            DofY = DofY - 15
        else:
            ThS = "ขึ้น "
        
        th_lunar_date = f"{ThS}{DofY} ค่ำ เดือน {ThM}"
    
    elif NbLDayYear == 355:
        RDayLY = RDayPrev + the_days_in_a_solar_year(input_date)
        DofY = DayFromOne
        
        for j in range(1, 15):
            ThM = j
            
            if j == 1:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 2:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 3:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 4:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 5:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 6:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 7:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 8:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 9:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 10:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 11:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 12:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 13:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 14:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
        
        if ThM > 12:
            ThM = ThM - 12
            ThZ = 1
        else:
            ThZ = 0
        
        if DofY > 15:
            ThS = "แรม "
            DofY = DofY - 15
        else:
            ThS = "ขึ้น "
        
        th_lunar_date = f"{ThS}{DofY} ค่ำ เดือน {ThM}"
    
    elif NbLDayYear == 384:
        RDayLY = RDayPrev + the_days_in_a_solar_year(input_date)
        DofY = DayFromOne
        
        for j in range(1, 15):
            ThM = j
            
            if j == 1:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 2:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 3:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 4:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 5:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 6:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 7:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 8:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 9:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 10:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 11:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 12:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 29
            elif j == 13:
                if DofY <= 30 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
            elif j == 14:
                if DofY <= 29 and DofY > 0:
                    break
                else:
                    DofY = DofY - 30
        
        if ThM > 13:
            ThM = ThM - 13
            ThZ = 1
        else:
            ThZ = 0
        
        if ThM == 9:
            ThM = 88
        elif ThM == 10:
            ThM = 9
        elif ThM == 11:
            ThM = 10
        elif ThM == 12:
            ThM = 11
        elif ThM == 13:
            ThM = 12
        
        if DofY > 15:
            ThS = "แรม "
            DofY = DofY - 15
        else:
            ThS = "ขึ้น "
        
        th_lunar_date = f"{ThS}{DofY} ค่ำ เดือน {ThM}"
    
    return th_lunar_date

# 9. th_lunar_date Function
def th_lunar_date(input_date):
    """
    คำนวณวันที่ตามปฏิทินจันทรคติไทยจากวันที่ที่ให้มา.

    ฟังก์ชันนี้จะแปลงวันที่ในรูปแบบปฏิทินแบบสากล (Gregorian) เป็นรูปแบบปฏิทินจันทรคติไทย. 
    รองรับการคำนวณวันที่ตั้งแต่ปี ค.ศ. 1903 (พ.ศ. 2446) ถึง ค.ศ. 2460 (พ.ศ. 3003).
    วันที่ที่ไม่อยู่ในช่วงนี้จะถูกคืนค่าเป็น "ไม่รองรับ".

    Parameters:
    input_date (datetime.date): วันที่ที่ต้องการคำนวณในรูปแบบปฏิทินจันทรคติไทย.

    Returns:
    str: วันที่ตามปฏิทินจันทรคติไทยหรือ "ไม่รองรับ" หากวันที่อยู่นอกช่วงที่รองรับ.

    ตัวอย่าง:
    >>> th_lunar_date(datetime.date(2023, 1, 1))
    'ขึ้น 1 ค่ำ เดือน 5'
    """

    # ตรวจสอบว่าปีอยู่ในช่วงที่รองรับหรือไม่
    if input_date.year < 1903 or input_date.year > 2460:
        return "ไม่รองรับ"

    # คำนวณวันที่เริ่มต้นจาก sDate
    # ข้อมูล sDate ควรมีในรูปแบบ [(ปี, เดือน, วัน), ...]
    sDate = [
        datetime(1902, 11, 30),
        datetime(1912, 12, 8),
        datetime(1902, 11, 30),
        datetime(1912, 12, 8),
        datetime(1922, 11, 19),
        datetime(1932, 11, 27),
        datetime(1942, 12, 7),
        datetime(1952, 11, 16),
        datetime(1962, 11, 26),
        datetime(1972, 12, 5),
        datetime(1982, 11, 15),
        datetime(1992, 11, 24),
        datetime(2002, 12, 4),
        datetime(2012, 11, 13),
        datetime(2022, 11, 23),
        datetime(2032, 12, 2),
        datetime(2042, 12, 12),
        datetime(2052, 11, 21),
        datetime(2062, 12, 1),
        datetime(2072, 12, 9),
        datetime(2082, 11, 20),
        datetime(2092, 11, 28),
        datetime(2102, 12, 9),
        datetime(2112, 11, 18),
        datetime(2122, 11, 28),
        datetime(2132, 12, 7),
        datetime(2142, 11, 17),
        datetime(2152, 11, 26),
        datetime(2162, 12, 6),
        datetime(2172, 11, 15),
        datetime(2182, 11, 25),
        datetime(2192, 12, 4),
        datetime(2202, 12, 15),
        datetime(2212, 11, 24),
        datetime(2222, 12, 4),
        datetime(2232, 12, 12),
        datetime(2242, 11, 23),
        datetime(2252, 12, 1),
        datetime(2262, 12, 11),
        datetime(2272, 11, 20),
        datetime(2282, 11, 30),
        datetime(2292, 12, 9),
        datetime(2302, 11, 20),
        datetime(2312, 11, 29),
        datetime(2322, 12, 9),
        datetime(2332, 11, 18),
        datetime(2342, 11, 28),
        datetime(2352, 12, 7),
        datetime(2362, 12, 17),
        datetime(2372, 11, 26),
        datetime(2382, 12, 6),
        datetime(2392, 12, 14),
        datetime(2402, 11, 25),
        datetime(2412, 12, 3),
        datetime(2422, 12, 13),
        datetime(2432, 11, 23),
        datetime(2442, 12, 2),
        datetime(2452, 12, 11),
    ]

    BeginDate = max((d for d in sDate if d.year <= input_date.year), default=None)

    if not BeginDate:
        return "ไม่รองรับ"

    # นับวารถึงปีก่อนหน้าปีปัจจุบัน
    DayInYear = sum(The_days_in_a_lunar_year(y) for y in range(BeginDate.year + 1, input_date.year))
    BeginDate += timedelta(days=DayInYear)

    # จำนวนวารที่เหลืออยู่ของปี นับจาก ขึ้น 1 ค่ำเดือน 1
    RDayPrev = (datetime(BeginDate.year, 12, 31) - BeginDate).days
    # จำนวนวันของปีที่ถึงวันที่ที่กำหนด
    DayOfYear = (input_date - datetime(input_date.year, 1, 1)).days
    # จำนวนวารจากขึ้น ๑ ค่ำ เดือน ๑ + จำนวนวารที่เหลือในปีถัดไป
    DayFromOne = RDayPrev + DayOfYear + 1
    # จำนวนวารของปี
    NbLDayYear = The_days_in_a_lunar_year(input_date.year)

    # คำนวณจันทรคติ
    th_lunar_date = calculate_th_lunar_date(NbLDayYear, RDayPrev, input_date, DayFromOne)

    return th_lunar_date

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
def th_zodiac(input_date, output_type=1, output_class=True):
    """
   คำนวณราศีตามวันที่ไทย

    Args:
        input_date (datetime.datetime): วันที่ที่ต้องการคำนวณราศี
        output_type (int, optional): ประเภทผลลัพธ์ที่ต้องการคืนค่า (1 = ชื่อราศีตามภาษาไทย, 2 = ชื่อราศีตามภาษาอังกฤษ, 3 = เลขราศี). Default เป็น 1.
        output_class (bool, optional): สถานะของผลลัพธ์ที่จะคืนค่า (True = คืนค่าแบบคลาสหรือเดือน, False = คืนค่าแบบคลาสหรือเดือนหลังวันตรงกับวันตรุษจีนในปีนั้น). Default เป็น True.

    Returns:
        str or int: ชื่อราศีตามประเภทผลลัพธ์และสถานะที่ต้องการ

    """
    Zodiac = {
        1: ["ชวด", "ฉลู", "ขาล", "เถาะ", "มะโรง", "มะเส็ง", "มะเมีย", "มะแม", "วอก", "ระกา", "จอ", "กุน"],
        2: ["RAT", "OX", "TIGER", "RABBIT", "DRAGON", "SNAKE", "HORSE", "GOAT", "MONKEY", "ROOSTER", "DOG", "PIG"],
        3: list(range(1, 13))
    }

    newyear_lunar_date = find_thai_newyear_lunar_date(input_date.year)

    result = input_date.year % 12
    if result - 3 < 1:
        result = result - 3 + 12
    else:
        result = result - 3

    if ((input_date >= newyear_lunar_date) or (output_class == False)):
        return Zodiac[output_type][result-1]
    else:
        return Zodiac[output_type][result-2]

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
    if athikamas(input_date.year):
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
    else:
        return ""