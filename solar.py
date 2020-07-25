from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import json

driver = webdriver.Chrome('C:\Monitoring\chromedriver')
weekday = ['월', '화', '수', '목', '금', '토', '일']

# SMP 가격 받아오기
# driver.get('http://onerec.kmos.kr/portal/rec/selectRecSMPList.do?key=1965')
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# smp = soup.select('#div1_t > table > tfoot > tr:nth-child(3) > td:nth-child(8)')

dt = datetime.now()
today = f'{dt.strftime("%m.%d")}({weekday[dt.weekday()]})'
smp = requests.get(
    "http://onerec.kmos.kr/portal/rec/selectRecSMPList.do?key=1965")
smpPrice = smp.text.split(f'가중평균\n{today}')[1].split('"')[0].split("\n")[1]
smpAvgPrice = 'SMP 평균 가격: ' + str(smpPrice) + '원'

# REC 가격 받아오기
rec = requests.get("https://www.mal-eum.com/rec/trend")
stringArray = rec.text.split('recdata = ')[1].split(';')[0]
realArray = json.loads(stringArray)
RecPrice = realArray[len(realArray)-1]['average_price']
recprint = 'REC 평균 가격: ' + str("{:,}".format(RecPrice)) + '원'

# 마이산태양광
driver.get('http://weblink.hex.co.kr/kor/Customer/default.aspx')
driver.find_element_by_name("ctl00$main$txt_ID").send_keys("마이산")
driver.find_element_by_name("ctl00$main$txt_PW").send_keys("0000")
driver.find_element_by_xpath('//*[@id="ctl00_main_btn_Login"]').click()

driver.get('http://weblink.hex.co.kr/kor/Reports/default.aspx?p=r1')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
abc = soup.select('#ctl00_main_lbl_DailySum')

temp = abc[0].text[0:len(abc[0].text)-4]
if len(abc[0].text) > 8:
    temp1 = temp.split(',')[0]
    temp2 = temp.split(',')[1]
    temp = temp1+temp2

# 발전량이 0으로 나올때 밤이거나 시스템에 문제가 발생했을때
if temp == '':
    n = q1 = 0
    m = a = 0
    smpa = 'ʕ·ᴥ·ʔ  Error  ʕ·ᴥ·ʔ'
    bb = '마이산태양광 문제 발생' + '%0A'+'사이트를 확인하세요!'
else:
    smpa = '마이산 발전량: '+abc[0].text
    n = int(temp)
    q1 = n
    fixed_price = 179.165
    m = round(n*fixed_price)
    a = m
    m = "{:,}".format(m)
    bb = '마이산태양광 장기계약 수익: ' + str(m) + '원'

# 빛고을태양광
driver.get('http://weblink.hex.co.kr/kor/Customer/default.aspx')
driver.find_element_by_name("ctl00$main$txt_ID").send_keys("빛고을태양광")
driver.find_element_by_name("ctl00$main$txt_PW").send_keys("0000")
driver.find_element_by_xpath('//*[@id="ctl00_main_btn_Login"]').click()

driver.get('http://weblink.hex.co.kr/kor/Reports/default.aspx?p=r1')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
abc = soup.select('#ctl00_main_lbl_DailySum')

temp = abc[0].text[0:len(abc[0].text)-4]
if len(abc[0].text) > 8:
    temp1 = temp.split(',')[0]
    temp2 = temp.split(',')[1]
    temp = temp1+temp2

# 발전량이 0으로 나올때 밤이거나 시스템에 문제가 발생했을때
if temp == '':
    n = q2 = 0
    m = b = 0
    smpb = 'ʕ·ᴥ·ʔ  Error  ʕ·ᴥ·ʔ'
    cc = '빛고을태양광 문제 발생' + '%0A'+'사이트를 확인하세요!'
else:
    smpb = '빛고을태양광 발전량: '+abc[0].text
    n = int(temp)  # 하루동안 생산한 전력량
    q2 = n
    fixed_price = 179.165
    m = round(n*fixed_price)
    b = m
    m = "{:,}".format(m)
    cc = '빛고을태양광 장기계약 수익: ' + str(m) + '원'

# 자연농장태양광
driver.get('http://weblink.hex.co.kr/kor/Customer/default.aspx')
driver.find_element_by_name("ctl00$main$txt_ID").send_keys("자연농장")
driver.find_element_by_name("ctl00$main$txt_PW").send_keys("0000")
driver.find_element_by_xpath('//*[@id="ctl00_main_btn_Login"]').click()

driver.get('http://weblink.hex.co.kr/kor/Reports/default.aspx?p=r1')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
abc = soup.select('#ctl00_main_lbl_DailySum')

temp = abc[0].text[0:len(abc[0].text)-4]
if len(abc[0].text) > 8:
    temp1 = temp.split(',')[0]
    temp2 = temp.split(',')[1]
    temp = temp1+temp2

# 발전량이 0으로 나올때 자정이 지나서 접속했거나 시스템에 문제가 발생했을때
if temp == '':
    n = q3 = 0
    m = c = c1 = 0
    smpc = 'ʕ·ᴥ·ʔ  Error  ʕ·ᴥ·ʔ'
    dd = '자연농장태양광 문제 발생' + '%0A' + '사이트를 확인하세요!'
else:
    smpc = '자연농장태양광 발전량: '+abc[0].text
    n = int(temp)
    q3 = n
    m = float(smpPrice)
    x = round(n*m)
    xx = round(n*RecPrice*1.5/1000)
    c = x
    c1 = xx
    temp9 = "{:,}".format(x+xx)
    dd = '자연농장태양광 수익: ' + str(temp9) + '원'


# 형제태양광
driver.get('http://weblink.hex.co.kr/kor/Customer/default.aspx')
driver.find_element_by_name("ctl00$main$txt_ID").send_keys("형제태양광")
driver.find_element_by_name("ctl00$main$txt_PW").send_keys("0000")
driver.find_element_by_xpath('//*[@id="ctl00_main_btn_Login"]').click()

driver.get('http://weblink.hex.co.kr/kor/Reports/default.aspx?p=r1')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
abc = soup.select('#ctl00_main_lbl_DailySum')

temp = abc[0].text[0:len(abc[0].text)-4]
if len(abc[0].text) > 8:
    temp1 = temp.split(',')[0]
    temp2 = temp.split(',')[1]
    temp = temp1+temp2

# 발전량이 0으로 나올때 밤이거나 시스템에 문제가 발생했을때
if temp == '':
    n = q4 = 0
    m = d = d1 = 0
    smpd = 'ʕ·ᴥ·ʔ  Error  ʕ·ᴥ·ʔ'
    ee = '형제태양광 문제 발생'+'%0A' + '사이트를 확인하세요!'
else:
    smpd = '형제태양광 발전량: '+abc[0].text
    n = int(temp)
    q4 = n
    m = float(smpPrice)
    x = round(n*m)
    xx = round(n*RecPrice*1.5/1000)
    d = x
    d1 = xx
    temp10 = "{:,}".format(x+xx)
    ee = '형제태양광 수익: ' + str(temp10) + '원'

# 총발전량 총수익 계
x = a+b+c+d+c1+d1
y = q1+q2+q3+q4
temp = "{:,}".format(x)
y = "{:,}".format(y)

generate = '오늘 총 발전량: ' + str(y) + ' kWh'
hh = '오늘 총 수익: ' + str(temp) + '원'


# 텔레그램 전송
# 텔레그램 id 얻기: https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/getUpdates
# 텔레그램 전송하기: https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=1006172083&text=hi
youngan = 'https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=1065066573&text='
myoungsun = 'https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=807722409&text='
youngil = 'https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=1006172083&text='
moonsung = 'https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=1024930293&text='
jisung = 'https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=1011259901&text='
jaewan = 'https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=1008166078&text='
hogab = 'https://api.telegram.org/bot1057732762:AAElCINsv1bhcZZC7KNuKxyiv3d6dbmHwe0/sendMessage?chat_id=997388561&text='

r = time.localtime().tm_wday
time = str(datetime.today().year)+'년'+str(datetime.today().month) + \
    '월' + str(datetime.today().day)+'일'+'('+weekday[r]+')'+'의 태양광 수익'
text = time+'%0A'+'%0A'+smpAvgPrice+'%0A' + recprint+'%0A'+'%0A'+smpa+'%0A'+bb+'%0A'+'%0A'+smpb + \
    '%0A'+cc+'%0A'+'%0A'+smpc+'%0A'+dd+'%0A'+'%0A' + \
    smpd+'%0A'+ee+'%0A'+'%0A'+generate+'%0A'+hh

link = youngan + text
driver.get(link)

link = moonsung + text
driver.get(link)

link = jisung + text
driver.get(link)

link = jaewan + text
driver.get(link)

link = hogab + text
driver.get(link)

driver.quit()
