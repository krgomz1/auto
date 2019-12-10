def url_check(site, code):
    from selenium import webdriver
    import time
    # 크롬드라이버 열기
    driver = webdriver.Chrome('C://chromedriver.exe')

    # 3초 기다려라
    driver.implicitly_wait(3)

    # HCMS 사이트 열어라
    driver.get(site)

    # 로그인해라
    driver.find_element_by_name('ID').send_keys('krgomz')
    driver.find_element_by_name('PWD').send_keys('5T4r3e2w1q!')
    driver.find_element_by_id('btnLogin').click()

    # 해당 과정포팅 사이트
    site1 = 'http://hcms.hunet.co.kr/Porting/IndexList.aspx?partnerId=thermp&courseCd='
    site2 = '&pageIndex=0&pageSize=10&searchPartnerNm=&searchCourseNm=&searchCpPortingConfirmYn='

    # 맛보기 체커
    driver.get(site1 + code + site2)
    time.sleep(3)
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_Lvw_ctrl1_Div6').click()
    time.sleep(3)

    # 경고창 확인
    from selenium.common.exceptions import NoAlertPresentException
    try:
        driver.switch_to_alert().accept()

    except NoAlertPresentException as e:
        print("no alert"+ code)

    driver.quit()
    print(code, '완료')


code = []
code = input('과목코드를 입력하세요 : ').split()
print(len(code), '개 실행')

site1 = 'http://hcms.hunet.co.kr/'
for code1 in code:
    url_check(site1, code1)

print(len(code), '개 완료')