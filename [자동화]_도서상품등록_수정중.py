from selenium import webdriver

#크롬드라이버 열기
driver = webdriver.Chrome('C://chromedriver.exe')

#3초 기다려라
driver.implicitly_wait(3)

#HSM 사이트 열어라
driver.get('http://admin.hunet.co.kr/')

#로그인해라
driver.find_element_by_name('UserName').send_keys('krgomz')
driver.find_element_by_name('Password').send_keys('1A2s3d4f5g!')
driver.find_element_by_id('btnLogon').click()

#경고창 확인
from selenium.common.exceptions import NoAlertPresentException
try:
    driver.switch_to_alert().accept()

except NoAlertPresentException as e:
    print("로그인 완료")


#도서등록 공식
def book_reg(book_name):
    # 도서등록사이트 오픈
    driver.get('https://admin.hunet.co.kr/Mall/Goods/GoodsList.aspx')
    driver.find_element_by_id('ctl00_ContentPlaceHolder1_RegistGoods').click()

    # 도서 등록하기
    driver.find_element_by_name('ctl00$ContentPlaceHolder1$goodsName_nm').send_keys(book_name)
    driver.find_element_by_name('ctl00$ContentPlaceHolder1$normalPrice_num').send_keys(0)
    driver.find_element_by_name('ctl00$ContentPlaceHolder1$goldPrice_num').send_keys(0)
    driver.find_element_by_xpath(
        "//select[@name='ctl00$ContentPlaceHolder1$sale_category_cd']/option[text()='단과']").click()
    driver.find_element_by_xpath("//select[@name='ctl00$ContentPlaceHolder1$deliver_yn']/option[text()='배송']").click()
    driver.implicitly_wait(3)
    driver.find_element_by_name('ctl00$ContentPlaceHolder1$thu_goods_delivery_cnt').send_keys(1)
    driver.find_element_by_xpath(
        "//select[@name='ctl00$ContentPlaceHolder1$thu_goods_delivery_delivery_partner_id']/option[text()='해커스']").click()
    driver.find_element_by_xpath(
        "//select[@name='ctl00$ContentPlaceHolder1$thu_goods_delivery_logistics_partner_id']/option[text()='CJ택배']").click()
    driver.find_element_by_name('ctl00$ContentPlaceHolder1$RegistGoods').click()

    # 경고창 확인
    from selenium.common.exceptions import NoAlertPresentException
    try:
        driver.switch_to_alert().accept()

    except NoAlertPresentException as e:
        print("처리완료")

book_name = []
book_name = input('도서명 리스트를 입력하세요(;로 구분해주세요) : ').split(";")

print(len(book_name))
print(book_name)

act = []
act = input('실행하실려면 Y를 입력해주세요 : ')

if 'Y' or 'y' in act:
    for code1 in book_name:
        book_reg(code1)
else:
    print('다시 실행해주세요')