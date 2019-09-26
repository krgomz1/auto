# 모듈 추가
import pandas as pd
import time

# 날짜 변수 추가
today = time.strftime('%y%m%d')
this_month = int(time.strftime('%m')) - 1  #전월 데이터

# 매출 엑셀파일 불러오기
raw_df = pd.read_excel('D:/0. 원단위/★매출자료 접근.xlsx', sheet_name='Sheet1')

# 맵핑 엑셀파일 불러오기
map_df = pd.read_excel('D:/0. 원단위/`과목-CP사 맵핑-190828.xlsx', sheet_name='mapping Data')

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
df2 = df.rename(columns={'과목명(품목)': '맵핑용 과목명'})
df2['맵핑용 과목명'] = df2['맵핑용 과목명'].map(lambda x: x.lstrip('과목: '))
map_df = map_df.rename(columns={'과정명': '맵핑용 과목명'})

## 카테고리 및 CP사 맵핑하기
results = pd.merge(df2, map_df, on='맵핑용 과목명', how = 'left')
nan_rows = results[results['대분류명'].isnull()]

# 결과
writer = pd.ExcelWriter('D:/0. 원단위/매출 RAW/results_' + today + '_사전작업용.xlsx')
results.to_excel(writer, sheet_name='raw')
nan_rows.to_excel(writer, sheet_name='미맵핑')
writer.save()


"""
#  na값  추출하기
nan_rows = results[results['대분류명'].isnull()]
nan_rows

#  맵핑하기
s1 = pd.Series(['M', 'M','F','F','M'])
print(s1)
gender = {'M':0, 'F': 1}
print(s1.map(gender))

"""