from selenium import webdriver

#크롬드라이버 열기
driver = webdriver.Chrome('C://chromedriver.exe')

#3초 기다려라
driver.implicitly_wait(3)

#HSM 사이트 열어라
driver.get('https://ims.hunet.co.kr/Login/Index?appId=55f6a9f448614a62ba88132da2b48e90&returnUrl=https%3a%2f%2flms.hunet.co.kr%2fLogin.aspx&iframeUrl=')

#로그인해라
driver.find_element_by_name('UserName').send_keys('krgomz')
driver.find_element_by_name('Password').send_keys('1A2s3d4f5g!')
driver.find_element_by_id('btnLogon').click()

#업로드창으로 진입
driver.get('https://lms.hunet.co.kr/Process/Event/PopupProcessTermRegist.aspx?commonSeq=18417&menuCode=0102-D01&menuName=%uACFC%uC815%uAE30%uC218%uAD00%uB9AC&tableName=TLS_CLASS_PROCESS_TERM&culumnName=COMPANY_SEQ')