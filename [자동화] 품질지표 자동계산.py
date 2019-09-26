### 데이터 세팅 ###
# 데이터 설정
raw_file = 'D:/1. 업무/1. 과정관련/7. 품질검수용/20190828.xlsx'
gross_file = 'D:/1. 업무/1. 과정관련/7. 품질검수용/gross_raw_190828.xlsx'

### 1. 모듈 세팅 ###
# 모듈 추가
import pandas as pd
import time
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
plt.style.use('dark_background')
sns.set(style="darkgrid", palette="bright", font_scale=1.5)

# matplot 한글폰트 설정
plt.rcParams["font.family"] = 'nanumGothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12.
plt.rcParams['xtick.labelsize'] = 10.
plt.rcParams['ytick.labelsize'] = 10.
plt.rcParams['axes.labelsize'] = 12.

# 날짜 변수 추가
today = time.strftime('%y%m%d')
this_month = int(time.strftime('%m')) - 1  #전월 데이터

# 과정정보 데이터프레임 설정
df_raw = pd.read_excel(raw_file, sheet_name= '일반')

# 컬럼 값 수정
df_raw = df_raw.rename(columns = {'모바일\n지원' : '모바일 지원'})
df_raw = df_raw.rename(columns = {'대분류 ' : '대분류'})
df_raw = df_raw.rename(columns ={'교재유무 ' : '교재유무'})


### 3. 세금계산서 기준 매출/인원 수 정리 및 표준점수 화 ###
#데이터 수집
df_gross = pd.read_excel(gross_file, sheet_name= '총금액')
df_nums = pd.read_excel(gross_file, sheet_name= '인원수')
df_nums = df_nums.rename(columns ={'행 레이블' : '과정명'})

#세금계산서 총금액 및 수강인원 합치기
df_total = pd.merge(df_gross, df_nums, how='left', on = '과정명')

#컬럼 이름 일괄 변경
 # 개선방향
def change_col(y1, y2):
    y2+=1
    p_col = [[str(i)+'_x', str(i)+'_y'] for i in range(y1,y2)]
    a_col = [[str(i)+'_매출', str(i)+'_인원'] for i in range(y1,y2)]
    for i in range(len(p_col)):
        df_total = df_total.rename(columns ={p_col[i][0] : a_col[i][0]})
        df_total = df_total.rename(columns ={p_col[i][1] : a_col[i][1]})

 # 작동 확인
change_col(2015, 2019)

"""
for i in range (2015, 2020):
    col1 = str(i) + '_x'
    col11 = str(i) + '_매출'
    col2 = str(i) + '_y'
    col21 = str(i) + '_인원'
    df_total = df_total.rename(columns ={col1 : col11})
    df_total = df_total.rename(columns ={col2 : col21})
"""



# 등록연도 과정정리
df_y = df_raw[['과정명', '등록일']]

# 등록연도 날짜설정
pd.options.mode.chained_assignment = None  # default='warn'
df_y['등록일'] = df_y['등록일'].astype('datetime64[ns]')
df_y['등록연도'] = df_y['등록일'].dt.year

#등록연도 데이터프레임 설정
df_ys = df_y[['과정명', '등록연도']]

# 등록연도 병합
df_total_y01 = pd.merge(df_ys, df_total, how='left', on = '과정명')

#등록연도에 따른 평균
g9 = df_total_y01['2019_매출']
g8 = df_total_y01['2018_매출']
g7 = df_total_y01['2017_매출']
g6 = df_total_y01['2016_매출']

n9 = df_total_y01['2019_인원']
n8 = df_total_y01['2018_인원']
n7 = df_total_y01['2017_인원']
n6 = df_total_y01['2016_인원']


df_total_y01.loc[df_total_y01['등록연도'] >= 2019, '평균매출'] = g9
df_total_y01.loc[df_total_y01['등록연도'] >= 2018, '평균매출'] = (g9 + g8)/2
df_total_y01.loc[df_total_y01['등록연도'] >= 2017, '평균매출'] = (g9 + g8 + g7)/3
df_total_y01.loc[df_total_y01['등록연도'] < 2017, '평균매출'] = (g9 + g8 + g7 + g6)/4

df_total_y01.loc[df_total_y01['등록연도'] >= 2019, '평균인원'] = n9
df_total_y01.loc[df_total_y01['등록연도'] >= 2018, '평균인원'] = (n9 + n8)/2
df_total_y01.loc[df_total_y01['등록연도'] >= 2017, '평균인원'] = (n9 + n8 + n7)/3
df_total_y01.loc[df_total_y01['등록연도'] < 2017, '평균인원'] = (n9 + n8 + n7 + n6)/4

# 평균 인원, 매출 데이터 추출
df_avr = df_total_y01[['과정명', '평균인원', '평균매출' ]]
df_raw_avr = df_raw[['대분류', '중분류', '소분류','과정명']]
df_raw_avr = pd.merge(df_raw_avr, df_avr, how='left', on = '과정명')


# 평균 인원, 매출 소분류별 평균, 표준편차 추가
df_avr_mean = df_raw_avr.groupby(['소분류']).mean()
df_avr_std = df_raw_avr.groupby(['소분류']).std()

df_avr_std = df_avr_std.rename(columns = {'평균인원' : '소분류 인원 편차'})
df_avr_std = df_avr_std.rename(columns = {'평균매출' : '소분류 매출 편차'})

df_avr_mean = df_avr_mean.rename(columns = {'평균인원' : '소분류 인원 평균'})
df_avr_mean = df_avr_mean.rename(columns = {'평균매출' : '소분류 매출 평균'})

# 평균, 표준편차 데이터 merge
df_raw_avr = pd.merge(df_raw_avr, df_avr_mean, how='left', on = '소분류')
df_raw_avr = pd.merge(df_raw_avr, df_avr_std, how='left', on = '소분류')

# 2개년 평균 인원, 매출 소분류별 기준 표준점수 산정
df_raw_avr['인원 표준점수'] = ((df_raw_avr['평균인원']- df_raw_avr['소분류 인원 평균'])/df_raw_avr['소분류 인원 편차'])*10 + 50
df_raw_avr['매출 표준점수'] = ((df_raw_avr['평균매출']- df_raw_avr['소분류 매출 평균'])/df_raw_avr['소분류 매출 편차'])*10 + 50
df_raw_avr_stan = df_raw_avr[['과정명', '인원 표준점수', '매출 표준점수']]

# ★표준 졈수 결과★
df_x = df_raw_avr_stan
df_x = df_x.fillna(25)

### 3. 환급과정 점수화
# 환급과정 파일 정리
df_refund = df_raw[['중분류', '소분류', '과정명', '고용보험적용여부']]
df_refund['구분자'] = df_refund['중분류'] + "_" + df_refund['소분류']

# 환급과정 숫자정리
p_refund = df_refund.pivot_table(values = '과정명', index = '구분자', columns = '고용보험적용여부', aggfunc = 'count', fill_value = 0)

# 환급과정 점수화
p_refund['환급점수'] = (p_refund['N']/(p_refund['Y'] + p_refund['N']))*100
p_refund_r = pd.DataFrame(p_refund)
p_refund_r = p_refund_r['환급점수']

# ★환급과정 점수화 최종결과★
df_refund = pd.merge(df_refund, p_refund_r, how='left', on = '구분자')
df_refund_r2 = df_refund[['과정명', '환급점수']]

### 4. 모바일 점수화
# 모바일 과정 파일 정리
df_mo = df_raw[['중분류', '소분류', '과정명', '모바일 지원']]
df_mo['구분자'] = df_mo['중분류'] + "_" + df_mo['소분류']

# 모바일 여부 정리
mo_c = df_mo['모바일 지원']
df_mo.loc[mo_c == '학습연동', '모바일여부'] = 'Y'
df_mo.loc[mo_c == '부가제공', '모바일여부'] = 'Y'
df_mo.loc[mo_c == '-', '모바일여부'] = 'N'

# 모바일 점수화
p_mo = df_mo.pivot_table('과정명', '구분자', '모바일여부', aggfunc = 'count', fill_value = 0)
p_mo['점수'] = (p_mo['N']/(p_mo['Y'] + p_mo['N']))*100
p_mo_r = pd.DataFrame(p_mo)
p_mo_r = p_mo_r['점수']

# ★모바일 점수 최종 결과★
df_mo = pd.merge(df_mo, p_mo_r, how = 'left', on ='구분자')
df_mo.loc[df_mo['모바일여부'] =='Y', '모바일점수'] =  df_mo['점수'] * 1
df_mo.loc[df_mo['모바일여부'] =='N', '모바일점수'] =  df_mo['점수'] * 0
df_mo_r2 = df_mo[['과정명', '모바일점수']]

### 5. 개발연도 점수화
# 개발연도 과정정리
df_y = df_raw[['과정명', '개발년월']]

# 개발연도 날짜 정리
pd.options.mode.chained_assignment = None  # default='warn'
df_y['개발년월'] = df_y['개발년월'].astype('datetime64[ns]')
df_y['개발연도'] = df_y['개발년월'].dt.year

# 개발연도 점수화
df_ys = df_y[['과정명', '개발연도']]

ys = df_ys.개발연도

df_ys.loc[ys >= 2018, '개발연도 점수'] = 100
df_ys.loc[(ys < 2018) & (ys >= 2016) , '개발연도 점수'] = 50
df_ys.loc[(ys >= 2013) & (ys < 2016), '개발연도 점수'] = 20
df_ys.loc[ys < 2013, '개발연도 점수'] = 0

# ★개발연도 점수 최종 결과★
df_ys_r = df_ys[['과정명', '개발연도 점수']]

# ★학습시간 점수 최종 결과★
df_time = df_raw[['과정명', '컨텐츠 시간']]
df_time.loc[df_time['컨텐츠 시간'] >= 8, '시간점수'] = 50
df_time.loc[df_time['컨텐츠 시간'] < 8, '시간점수'] = 0
df_time_re = df_time[['과정명', '시간점수']]


## 최종 점수 취합 ##
# 과정별 품질점수 종합
df_result1 = df_x           # 매출,학습자 수 점수
df_result2 = df_refund_r2   # 환급점수
df_result3 = df_mo_r2       # 모바일 점수
df_result4 = df_ys_r        # 개발연도 점수
df_result5 = df_time_re     # 학습시간 점수

# 과정별 품질점수 취합
df_result0 = df_x

for i in [df_result2, df_result3, df_result4, df_result5]:
    df_result0 = pd.merge(df_result0, i, how ='left', on ='과정명')

# 종합점수 산정
col1 = df_result0['인원 표준점수']
col2 = df_result0['매출 표준점수']
col3 = df_result0['환급점수']
col4 = df_result0['모바일점수']
col5 = df_result0['개발연도 점수']
col6 = df_result0['시간점수']

df_result0['종합점수'] = col1 + col2 + col3 + col4 + col5 + col6

# 종합점수 카테고리 추가
df_cat = df_raw[['중분류','소분류', '과정명']]
df_cat['구분자'] = df_cat['중분류'] + '_' + df_cat['소분류']
df_result1 = pd.merge(df_result0, df_cat, how = 'left', on = '과정명')


# 종합점수 평균, 표준편차
df_total = df_result1[['구분자', '과정명', '종합점수']]
df_total_mean = df_total.groupby('구분자').mean()
df_total_std = df_total.groupby('구분자').std()

df_total_mean = df_total_mean.rename(columns = {'종합점수' : '종합점수 평균' })
df_total_std = df_total_std.rename(columns = {'종합점수' : '종합점수 편차' })

# 종합점수 평균, 표준편차 추가 병합
df_total_re01 = pd.merge(df_total, df_total_mean, how ='left', on = '구분자' )
df_total_re = pd.merge(df_total_re01, df_total_std, how ='left', on = '구분자' )

# 종합점수 표준점수화
val01 = df_total_re['종합점수']
val02 = df_total_re['종합점수 평균']
val03 = df_total_re['종합점수 편차']

df_total_re['종합 표준점수'] = ((val01 - val02)/val03)*10 +50
df_total_re1 = df_total_re[['과정명', '종합 표준점수']]

# 최종 점수표에 추가 및 최종 리포트
df_result2 = pd.merge(df_result0, df_total_re1, how = 'left', on = '과정명')
df_result3 = df_result2[['과정명', '인원 표준점수', '매출 표준점수', '모바일점수', '개발연도 점수', '시간점수', '종합 표준점수']]
df_result3 = pd.merge(df_result3, df_cat, how='left', on='과정명')
df_score = df_result3.drop_duplicates()


# 파일로저장
file_path = 'D:/1. 업무/1. 과정관련/7. 품질검수용/과정별 품질점수/과정별 품질점수_'

writer = pd.ExcelWriter(file_path + today + 'ver1.5.xlsx')

df_score.to_excel(writer, sheet_name='score')
writer.save()