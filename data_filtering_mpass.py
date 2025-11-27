import pandas as pd

# 데이터 불러오기
df = pd.read_csv("서울교통공사_외국인 관광객 기간권 일별 통행통계_20241231.csv",encoding='cp949')

# 데이터 정보
# df.info()
# print(df.head())
# print(df.isnull().sum())               # 결측치 : 사용일수구분 3
# print(df[df.isnull().any(axis=1)])     # 결측치 포함된 데이터 확인

# 결측치 포함된 행 제거
df_clean = df.dropna()               
# print(df_clean.isnull().sum())
# df_clean.info()

# 승차와 하차 모두 0인 행 제거
df_clean = df_clean = df[~((df['승차건수'] == 0) & (df['하차건수'] == 0))]
# df_clean.info()

# 정제된 데이터 저장
df_clean.to_csv("Mpass_정제.csv", index=False, encoding="utf-8-sig")