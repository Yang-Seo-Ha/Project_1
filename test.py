import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("1회권 외국인 일별통행통계")

df = df.drop(columns=['권종'])

time_cols = [c for c in df.columns if c.endswith('시')]
df['월'] = pd.to_datetime(df['수송일자']).dt.month

df_board = df[df['승하차구분'] == '승차']
monthly_hour = df_board.groupby('월')[time_cols].sum()

plt.figure(figsize=(18,8))

for month in monthly_hour.index:
    plt.plot(time_cols, monthly_hour.loc[month], marker='o', label=f'{month}월')

plt.xticks(rotation=45)
plt.xlabel("시간대 (시)")
plt.ylabel("승차 인원수 (명)")
plt.title("월별 시간대별 승차 인원 프로파일")
plt.legend()
plt.grid(alpha=0.3)
plt.show()