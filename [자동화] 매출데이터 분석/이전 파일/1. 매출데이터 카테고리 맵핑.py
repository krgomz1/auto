
# 판다스 모듈 추가
import pandas as pd
import time

#오늘 날짜
today = time.strftime('%y%m%d')

# 엑셀파일 불러오기
df1 = pd.read_excel('D:/1. 업무/2. 기획 및 보고/`19년/190723_MIR/1. RAW.xlsx', sheet_name='Sheet1')
df2 = pd.read_excel('D:/1. 업무/2. 기획 및 보고/`19년/190723_MIR/2. mapping.xlsx', sheet_name='mapping Data')

# 두 데이터 합치기(raw 데이터에 맵핑파일 추가
results=df1.merge(df2,on='맵핑용 과목명')

# 다른이름으로 저장하기
results.to_excel('D:/1. 업무/2. 기획 및 보고/`19년/190723_MIR/3.result_'+today+'.xlsx',sheet_name='Sheet1')