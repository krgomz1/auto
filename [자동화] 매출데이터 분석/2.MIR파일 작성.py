file_name = "raw_20200213.xlsx"

# 모듈 추가
import pandas as pd
import time

# 날짜 변수 추가
today = time.strftime('%y%m%d')
this_month = 12
# int(time.strftime('%m')) - 1  #전월 데이터로 만들기

# 매출 엑셀파일 불러오기
raw_df = pd.read_excel('D:/0. 원단위/매출 RAW/'+file_name, sheet_name='Sheet1')

# 맵핑 엑셀파일 불러오기
map_df = pd.read_excel('D:/0. 원단위/`과목-CP사 맵핑-191001.xlsx', sheet_name='mapping Data')

# raw_df 열 삭제
del_cols = ['정산년월', '학습시작일', '단가', '공급가액', '세액', '튜터비',
            '저작권료', 'cp사정산금액', '마케팅수수료', '제휴사명']

for col in del_cols :
    del raw_df[col]

df = raw_df[raw_df['도입여부'] != '온라인과정X']

# 날짜 정리하기
pd.options.mode.chained_assignment = None  # default='warn'
df['계산서발행일'] = df['계산서발행일'].astype('datetime64[ns]')
df['매출연도'] = df['계산서발행일'].dt.year  #매출연도 추가
df['매출월'] = df['계산서발행일'].dt.month   #매출월 추가

# 14년 이후 매출데이터만 추출
df = df[df['매출연도'] > 2014 ]

# 매핑을 위해 데이터 정리
df['과목명(품목)'] = df['과목명(품목)'].map(lambda x: x.lstrip('과목: '))
df2 = df.rename(columns={'과목명(품목)': '맵핑용 과목명'})
map_df = map_df.rename(columns={'과정명': '맵핑용 과목명'})


## 카테고리 및 CP사 맵핑하기
results = pd.merge(df2, map_df, on='맵핑용 과목명', how = 'left')

# 자체 도입 분류 추가
results.loc[results.제휴사명 == '휴넷', '자체/도입'] = '자체'
results.loc[results.제휴사명 == '제외', '자체/도입'] = '제외'
results.loc[(results.제휴사명 != '제외') & (results.제휴사명 != '휴넷'), '자체/도입'] = '도입'

# 동기 비교용 데이터 만들기
results1 = results[results['대분류명'] != '제외']
results2 = results1[results1['자체/도입'] != '제외']
results3 = results2[results2['매출월'] <= this_month]

# 피벗테이블용 자체/도입 구분하기
results3_in = results3[results3['자체/도입'] == '자체']
results3_out = results3[results3['자체/도입'] == '도입']

# 이름단축
co = results3
co_in = results3_in
co_out = results3_out

## 피벗 데이터 만들기
#자체/도입 매출
summ = co.pivot_table(values=['총금액','학습자수'], index= '자체/도입', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Sales = co.pivot_table(values='총금액', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Num = co.pivot_table(values='학습자수', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)

#자체
Cate_Sales_in = co_in.pivot_table(values='총금액', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Num_in = co_in.pivot_table(values='학습자수', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)

#도입
Cate_Sales_out = co_out.pivot_table(values='총금액', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)
Cate_Num_out = co_out.pivot_table(values='학습자수', index= '대분류명', columns= '매출연도', aggfunc='sum', fill_value= 0)

# 저장위치 설정
save_path = 'D:/0. 원단위/매출 RAW/'

# raw 데이터 결과 값 저장하기
writer = pd.ExcelWriter(save_path + 'results_' + today + '_최종'+ '.xlsx')
co.to_excel(writer, sheet_name='raw')
summ.to_excel(writer, sheet_name='종합')
Cate_Sales.to_excel(writer, sheet_name='종합 카테고리별 매출')
Cate_Num.to_excel(writer, sheet_name='종합 카테고리별 수강생 수')
Cate_Sales_in.to_excel(writer, sheet_name='자체 카테고리별 매출')
Cate_Num_in.to_excel(writer, sheet_name='자체 카테고리별 수강생 수')
Cate_Sales_out.to_excel(writer, sheet_name='도입 카테고리별 매출')
Cate_Num_out.to_excel(writer, sheet_name='도입 카테고리별 수강생 수')
writer.save()

## 그래프 만들기
# matplot 한글폰트 설정
from matplotlib import pyplot as plt
import numpy as np
plt.rcParams["font.family"] = 'nanumGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12.
plt.rcParams['xtick.labelsize'] = 10.
plt.rcParams['ytick.labelsize'] = 10.
plt.rcParams['axes.labelsize'] = 12.

   ## 총 매출
    #그래프 숫자 세팅
fig, axes = plt.subplots(ncols=2, nrows=3, figsize = (20,18))

    # 변수 세팅
cat_lar = co.대분류명.unique()
g_loc = range(331, 338)

    # 여러개 설정
for g, c in zip(cat_lar, g_loc):
    plt.subplot(c)
    cat = g
    plt.plot(Cate_Sales.loc[cat])
    plt.xlabel('연도')
    plt.ylabel('매출')
    plt.xticks(np.arange(2015, 2020))
    plt.title(cat + ' 연도별 총매출')

    # 그림으로 저장
fig.savefig(save_path + 'graph/' + str(this_month) + '월 기준 연도별 동기 총 매출 추이_'+ today +'.png', format='png')

# 자체
    #그래프 숫자 세팅
fig, axes = plt.subplots(ncols=2, nrows=3, figsize = (20,18))

    # 변수 세팅
cat_lar = co_in.대분류명.unique()
g_loc = range(321, 327)

    # 여러개 설정
for g, c in zip(cat_lar, g_loc):
    plt.subplot(c)
    cat = g
    plt.plot(Cate_Sales_in.loc[cat])
    plt.xlabel('매출연도')
    plt.ylabel('총금액')
    plt.xticks(np.arange(2015, 2020))
    plt.title(cat + ' 연도별 자체 매출')

    # 그림으로 저장
fig.savefig(save_path + 'graph/' + str(this_month) + '월 기준 연도별 동기 자체 매출 추이_'+ today +'.png', format='png')

# 도입
#그래프 숫자 세팅
fig, axes = plt.subplots(ncols=3, nrows=2, figsize = (20,18))

# 변수 세팅
cat_lar = co_out.대분류명.unique()
g_loc = range(331, 338)

# 여러개 설정
for g, c in zip(cat_lar, g_loc):
    plt.subplot(c)
    cat = g
    plt.plot(Cate_Sales_out.loc[cat])
    plt.xlabel('매출연도')
    plt.ylabel('총금액')
    plt.xticks(np.arange(2015, 2020))
    plt.title(cat + ' 연도별 도입 매출')

# 그림으로 저장
fig.savefig(save_path + 'graph/' + str(this_month) + '월 기준 연도별 동기 도입 매출 추이_'+ today +'.png', format='png')