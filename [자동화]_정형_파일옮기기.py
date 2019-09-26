#파일 옮기기
import shutil
import time
today = time.strftime('%Y%m%d')

old_path = 'C:/Users/krgomz/Downloads/'
new_path = 'D:/1. 업무/1. 과정관련/0. 과정리스트/'
O_file_name = 'INTERNAL_EDUCATION_LIST_BIZ_' + today + '.xls'

# 정형과정 리스트
shutil.move(old_path + O_file_name, new_path + O_file_name)