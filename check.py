import pandas as pd

df = pd.read_csv('서울교통공사_외국인 관광객 기간권 일별 통행통계_20241231.csv', encoding ='cp949')
print(df.info())
print(df.head())
