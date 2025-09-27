import requests
import pandas as pd


#  굥기 선행지수 데이터 불러오기.
API_KEY = 'FPX1UX6MZ33NQFIM4HHK'  # 발급받은 API 키
STAT_CODE = '901Y067'     # 경기종합지수
ITEM_CODE = 'I16E'        # 선행지수 순환변동치
START = '202401'          # 예: 2000년 1월
END = '202508'            # 예: 2025년 8월

url = f"https://ecos.bok.or.kr/api/StatisticSearch/{API_KEY}/json/kr/1/100/{STAT_CODE}/M/{START}/{END}/{ITEM_CODE}"
resp = requests.get(url)
data = resp.json().get('StatisticSearch', {}).get('row', [])

df = pd.DataFrame(data)
df = df[['TIME', 'DATA_VALUE']].rename(columns={'TIME': '날짜', 'DATA_VALUE': '선행지수_순환변동치'})
print(df)

# 코스피 지수 불러오기
import requests
import pandas as pd
import matplotlib.pyplot as plt



API_KEY = 'FPX1UX6MZ33NQFIM4HHK'

start, end = '202401', '202508'
stat_code = "901Y014"   # 주식시장(월,년)
item_code = "1070000"   # 코스피 종가

# ECOS API URL (통계표코드, 주기, 항목코드, 기간 지정)
url_kospi = f"https://ecos.bok.or.kr/api/StatisticSearch/{API_KEY}/json/kr/1/1000/{stat_code}/M/{start}/{end}/{item_code}"

res_kospi = requests.get(url_kospi).json()
rows_kospi = res_kospi.get('StatisticSearch', {}).get('row', [])

if not rows_kospi:
    raise ValueError("코스피 데이터가 없습니다. 통계 코드와 기간을 확인하세요.")

df_kospi = pd.DataFrame(rows_kospi)[['TIME','DATA_VALUE']]
df_kospi['날짜'] = pd.to_datetime(df_kospi['TIME'], format='%Y%m')
df_kospi['코스피'] = df_kospi['DATA_VALUE'].astype(float)

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# 한글 폰트 설정 (Mac 기준)
plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

# ---- 데이터 준비 ----
# df_kospi : 코스피 데이터프레임 ['날짜','코스피']
# df : 경기선행지수 데이터프레임 ['날짜','선행지수_순환변동치']

df_kospi['날짜'] = pd.to_datetime(df_kospi['날짜'], format='%Y%m')
df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m')

import matplotlib.pyplot as plt
import pandas as pd

# 한글 폰트 설정 (Mac 기준)
plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

# 날짜 시계열 변환
df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m')
df_kospi['날짜'] = pd.to_datetime(df_kospi['날짜'], format='%Y%m')

# ---- 이중 Y축 그래프 ----
fig, ax1 = plt.subplots(figsize=(12,6))

# (1) 왼쪽 y축: 경기선행지수
ax1.plot(df['날짜'], df['선행지수_순환변동치'],
         color='blue', marker='o', label='경기선행지수')
ax1.set_xlabel('날짜', fontsize=12)
ax1.set_ylabel('경기선행지수 (지수)', fontsize=12, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, linestyle='--', alpha=0.6)

# (2) 오른쪽 y축: 코스피 종가
ax2 = ax1.twinx()
ax2.plot(df_kospi['날짜'], df_kospi['코스피'],
         color='red', marker='s', label='코스피 종가')
ax2.set_ylabel('코스피 종가 (지수)', fontsize=12, color='red')
ax2.tick_params(axis='y', labelcolor='red')

# (3) 제목 및 범례
plt.title('경기선행지수 vs 코스피 종가 (2024.01 ~ 2025.08)', fontsize=14)

# 범례 두 개 합치기
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.show()
