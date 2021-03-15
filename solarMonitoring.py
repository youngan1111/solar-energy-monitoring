import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import time

solarFarm = {'자연농장태양광': os.getenv('natural'), '형제태양광': os.getenv('brother'),
             '빛고을태양광': os.getenv('light'), '마이산태양광': os.getenv('mountain')}
weekday = ['월', '화', '수', '목', '금', '토', '일']
message = ''

r = time.localtime().tm_wday
currentTime = str(datetime.today().year)+'년 '+str(datetime.today().month) + \
    '월' + str(datetime.today().day)+'일'+'('+weekday[r]+') ' + str(datetime.today(
    ).hour) + '시' + str(datetime.today().minute) + '분' + '의 태양광 발전현황'

for key, value in solarFarm.items():
    response = requests.post(
        "http://weblink.hex.co.kr/kor/webservice/real.asmx/RealData21", data={'_cbid': value})
    soup = BeautifulSoup(response.content, "html.parser")
    isGenerating = json.loads(soup.tdata['value'])[0]['Badge']

    message += '%0A' + key + ' 발전 ' + BeautifulSoup(isGenerating, "html.parser").get_text(
    ) + '%0A' + '현재 발전량: ' + soup.d_tdaily['value'][2:len(soup.d_tdaily['value'])-2] + ' kWh' + '%0A'

youngan = os.getenv('youngan')
link = youngan + currentTime + '%0A' + message
requests.get(link)
