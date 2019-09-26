from selenium import webdriver

path = 'D:/1. 업무/6. 도입업무/★과정정보 요청파일_190725.xlsx'

#크롬드라이버 열기
driver = webdriver.Chrome('C://chromedriver.exe')

#3초 기다려라
driver.implicitly_wait(3)

#HSM 사이트 열어라
taget_url = 'https://ims.hunet.co.kr/Login/Index?appId=55f6a9f448614a62ba88132da2b48e90&returnUrl=https%3a%2f%2flms.hunet.co.kr%2fLogin.aspx&iframeUrl='
driver.get(taget_url)

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