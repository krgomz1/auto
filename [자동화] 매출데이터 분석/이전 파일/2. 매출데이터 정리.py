"""
엑셀파일 정리
"""

#모듈 불러오기
import openpyxl
import time
import pandas as pd

#오늘 날짜
today = time.strftime('%y%m%d')

#대상파일 정의
filename = 'D:/1. 업무/2. 기획 및 보고/`19년/190723_MIR/result190724.xlsx'

#엑셀파일 정의
wb = openpyxl.load_workbook(filename)
sh1 = wb.worksheets[0]


#필요없는 열 지우기
sh1.delete_cols(1, 1)
sh1.delete_cols(14, 4)


#구분자 이름 변경하기
sh1['o1'].value = 'CP사'
sh1['p1'].value = '대분류명'
sh1['q1'].value = '중분류명'
sh1['r1'].value = '소분류명'

#수식 일괄 넣기/ 자체 도입 구분
i = 2
colM = len(sh1['a']) + 1

while i < colM :
    Cel = 'N' + str(i)
    obj = 'O' + str(i)
    trs = 'Q' + str(i)
    if sh1[trs].value == "제외" :
        sh1[Cel].value = "제외"
    elif sh1[obj].value == "휴넷":
        sh1[Cel].value = "자체"
    else :
        sh1[Cel].value = "도입"
    i = i + 1
    if i == colM:
        print("입력 완료")

#저장하기
wb.save(filename)