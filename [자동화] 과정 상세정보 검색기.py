# 모듈 및 공통변수 세팅
import win32com.client as win32
excel = win32.Dispatch('Excel.Application')
excel.Visible = False
import pandas as pd
import time
today = time.strftime('%Y%m%d')


#과목정보/과정정보 세팅

num = input("검색할 과정 수를 입력하세요 : ")
m_code =[]
j_code =[]
m_code = input('과목코드를 입력하세요 : ').split()
j_code = input('과정코드를 입력하세요 : ').split()

if len(m_code) != int(num) :
    print("갯수가 다릅니다.")
elif len(j_code) != int(num) :
    print("갯수가 다릅니다.")
elif len(m_code) != len(j_code) :
    print("갯수가 다릅니다.")
else :
    print('진행합니다.')

print(j_code, m_code)

# 데이터 프레임 만들기
df = pd.DataFrame({'과정코드' : j_code, '과목코드' : m_code})
df.to_excel('D:/temp/code_detail_'+ today + '.xls')

# 엑셀 파일 정리하기
wb = excel.Workbooks.Open(u'D:/temp/code_detail_'+ today + '.xls')
sh = wb.ActiveSheet
sh.Columns("A:A").Delete()          #열 삭제 찾았다~!!!! 대박
wb.Save()

# 파일 다운로드
from selenium import webdriver

path = 'D:/temp/code_detail_'+ today + '.xls'

#크롬드라이버 열기
driver = webdriver.Chrome('C://chromedriver.exe')

#3초 기다려라
driver.implicitly_wait(3)

#HSM 사이트 열어라
driver.get('https://ims.hunet.co.kr/Login/Index?appId=55f6a9f448614a62ba88132da2b48e90&returnUrl=https%3a%2f%2flms.hunet.co.kr%2fLogin.aspx&iframeUrl=')

#로그인해라
driver.find_element_by_name('UserName').send_keys('krgomz')
driver.find_element_by_name('Password').send_keys('5T4r3e2w1q!')
driver.find_element_by_id('btnLogon').click()

#비정형 통계 과정정보 업로드에 들어가서 파일을 다운로드 해라
driver.get('https://lms.hunet.co.kr/Statistics/Auto/AutoInsert.aspx?seq=336')

#업로드창에 파일 올리기
driver.find_element_by_id('ExcelFile').send_keys(path)
driver.find_element_by_id('btnSubmit').click()

#경고창에 승인하기
driver.switch_to.alert.accept()