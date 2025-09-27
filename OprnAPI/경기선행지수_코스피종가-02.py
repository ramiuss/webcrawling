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

# ---- 2개 그래프 나란히 ----
fig, axes = plt.subplots(1, 2, figsize=(16,6))

# (1) 코스피 종가
axes[0].plot(df_kospi['날짜'], df_kospi['코스피'],
             label='코스피 종가', marker='s', color='red')
axes[0].set_title('코스피 종가 (2024.01 ~ 2025.08)', fontsize=14)
axes[0].set_xlabel('날짜', fontsize=12)
axes[0].set_ylabel('지수', fontsize=12)
axes[0].legend()
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(True, linestyle='--', alpha=0.6)

# (2) 경기선행지수
axes[1].plot(df['날짜'], df['선행지수_순환변동치'],
             marker='o', linestyle='-', color='blue')
axes[1].set_title('경기선행지수 순환변동치 (2024.01 ~ 2025.08)', fontsize=14)
axes[1].set_xlabel('날짜', fontsize=12)
axes[1].set_ylabel('지수', fontsize=12)
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.show()
