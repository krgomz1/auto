"""
데이터 분석 시작 점
"""

# 데이터 프레임으로 만들기
import openpyxl
import time
import pandas as pd
import numpy as np

#matplotlib 한글 설정
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

print ('버전: ', mpl.__version__)
print ('설치 위치: ', mpl.__file__)
print ('설정 위치: ', mpl.get_configdir())
print ('캐시 위치: ', mpl.get_cachedir())
print ('설정파일 위치: ', mpl.matplotlib_fname())
font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
print(len(font_list))
font_list[:10]
[(f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name]


#대상파일 정의
filename = 'D:/1. 업무/2. 기획 및 보고/`19년/190723_MIR/result190724.xlsx'

#엑셀파일 정의
wb = openpyxl.load_workbook(filename)
sh1 = wb.worksheets[0]
today = time.strftime('%y%m%d')

#데이터 프레임 정의
df = pd.read_excel(filename)
s_month = [1,2,3,4,5,6]
s_month

df_samemonth = df[df['매출월'] == s_month()]
df_in = df[df['자체/도입'] == '자체']
df_out = df[df['자체/도입'] == '도입']

#데이터 연도별 통계
df.groupby('매출연도')['총금액'].sum()
year_gross = df.groupby('매출연도')['총금액'].sum()

font_path = 'C:\\Windows\\Fonts\\NanumGothicLight.ttf'
font_name = fm.FontProperties(fname=font_path, size=50).get_name()
print(font_name)
plt.rc('font', family=font_name)

year_gross.plot(kind = 'bar', rot =0);
plt.title('연도별 매출 증감')
plt.tight_layout()


# 피벗테이블

#values='대상값', index= '행', columns= '열', aggfunc='취합방식', fill_value= 빈값은?
#도입/자체 매출
summ = df.pivot_table(values=['총금액','학습자수'], index= '자체/도입', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Sales = df.pivot_table(values='총금액', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Num = df.pivot_table(values='학습자수', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)

Cate_Sales_in = df_in.pivot_table(values='총금액', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Num_in = df_in.pivot_table(values='학습자수', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)

Cate_Sales_out = df_out.pivot_table(values='총금액', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Num_out = df_out.pivot_table(values='학습자수', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)

#도입/자체 매출


# 엑셀로 내보내기
writer = pd.ExcelWriter('results_' + today + '.xlsx')
df.to_excel(writer, sheet_name='raw')
summ.to_excel(writer, sheet_name='종합')
Cate_Sales.to_excel(writer, sheet_name='카테고리별 매출')
Cate_Num.to_excel(writer, sheet_name='카테고리별 학습자')
Cate_Sales_in.to_excel(writer, sheet_name='자체 카테고리별 매출')
Cate_Num_in.to_excel(writer, sheet_name='자체 카테고리별 학습자')
Cate_Sales_out.to_excel(writer, sheet_name='도입 카테고리별 매출')
Cate_Num_out.to_excel(writer, sheet_name='도입 카테고리별 학습자')
writer.save()
