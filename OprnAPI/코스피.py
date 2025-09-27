import requests
import pandas as pd
import matplotlib.pyplot as plt

# 한글폰트 설정 (Mac 기준)
plt.rc('font', family='AppleGothic')
plt.rc('axes', unicode_minus=False)

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

# 그래프 그리기
plt.figure(figsize=(12,6))
plt.plot(df_kospi['날짜'], df_kospi['코스피'], label='코스피 종가', marker='s', color='red')

plt.title('코스피 종가 (2024.01 ~ 2025.08)', fontsize=14)
plt.xlabel('날짜', fontsize=12)
plt.ylabel('지수', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
