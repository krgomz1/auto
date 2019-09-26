# 모듈 추가
import pandas as pd
import time

#오늘 날짜
today = time.strftime('%y%m%d')
this_month = int(time.strftime('%m')) - 1  #전월 데이터

# 엑셀파일 불러오기
raw_df = pd.read_excel('D:/0. 원단위/★매출자료 접근.xlsx', sheet_name='Sheet1')
df2 = pd.read_excel('D:/1. 업무/2. 기획 및 보고/`19년/190723_MIR/2. mapping.xlsx', sheet_name='mapping Data')

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

edit_df = df[df['매출연도'] > 2014 ]   # 14년 이후 매출데이터만 추출

# 신규 카테고리 맵핑
edit_df = edit_df.replace('과목:','')
edit_df = edit_df.rename(columns={'과목명(품목)': '맵핑용 과목명'})
results = edit_df.merge(df2, on='맵핑용 과목명')

# 자체 도입 분류 추가
results.loc[results.CP사 == '휴넷', '자체/도입'] = '자체'
results.loc[results.CP사 == '제외', '자체/도입'] = '제외'
results.loc[(results.CP사 != '제외') & (results.CP사 != '휴넷'), '자체/도입'] = '도입'

# 동기 비교용 데이터 만들기
results1 = results[results['대분류명'] != '제외']
results2 = results1[results1['자체/도입'] != '제외']
results_SameMonth = results2[results2['매출월'] <= this_month]
results_SameMonth


# 피벗테이블용 자체/도입 구분하기
results_SameMonth_in = results_SameMonth[results_SameMonth['자체/도입'] == '자체']
results_SameMonth_out = results_SameMonth[results_SameMonth['자체/도입'] == '도입']

co = results_SameMonth
co_in = results_SameMonth_in
co_out = results_SameMonth_out

# 피벗테이블
#values='대상값', index= '행', columns= '열', aggfunc='취합방식', fill_value= 빈값은?
#자체/도입 매출

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

"""
#그래프 한글 설정
plt.rcParams["font.family"] = 'nanumGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12.
plt.rcParams['xtick.labelsize'] = 12.
plt.rcParams['ytick.labelsize'] = 12.
plt.rcParams['axes.labelsize'] = 12.

# 그래프용 데이터 설정
ax = co_out.groupby('매출연도')['총금액'].sum()
summ_plot = ax.plot(kind= 'bar')
"""

# 결과
writer = pd.ExcelWriter('D:/0. 원단위/매출 RAW/results_' + today + '.xlsx')
co.to_excel(writer, sheet_name='raw')
summ.to_excel(writer, sheet_name='종합')
Cate_Sales.to_excel(writer, sheet_name='종합 카테고리별 매출')
Cate_Num.to_excel(writer, sheet_name='종합 카테고리별 수강생 수')
Cate_Sales_in.to_excel(writer, sheet_name='자체 카테고리별 매출')
Cate_Num_in.to_excel(writer, sheet_name='자체 카테고리별 수강생 수')
Cate_Sales_out.to_excel(writer, sheet_name='도입 카테고리별 매출')
Cate_Num_out.to_excel(writer, sheet_name='도입 카테고리별 수강생 수')
writer.save()