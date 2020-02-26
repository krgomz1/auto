from selenium import webdriver


#크롬드라이버 열기
driver = webdriver.Chrome('C://chromedriver.exe')

#C:/Users/krgomz/Desktop/자동화 다운로드/   --> 목표 URL

#3초 기다려라
driver.implicitly_wait(3)

#HSM 사이트 열어라
driver.get('http://hsm.hunet.co.kr/Report/Lecture.aspx')

#로그인해라
driver.find_element_by_name('txtID').send_keys('krgomz')
driver.find_element_by_name('txtDbPass').send_keys('1Q2w3e4r5t!')
driver.find_element_by_name('ImageButton1').click()
driver.implicitly_wait(3)


#보고서 사이트에 들어가서 다운로드 클릭해라

driver.get('http://hsm.hunet.co.kr/Report/Lecture.aspx')


#상상마루 리스트
driver.find_element_by_id('ctl00_ContentPlaceHolder1_Report6_Button').click()
driver.implicitly_wait(30)
