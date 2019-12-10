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

#자료 동기화 페이지로 이동 (중복검사 우선, 중복 이상없으면 실행)
driver.get('https://lms.hunet.co.kr/Asp/Sync/Sync.aspx')
driver.find_element_by_id('ctl00_ContentPlaceHolder1_txtCompanySeq_1').send_keys('18417')
driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnStudyDTS_I').click()