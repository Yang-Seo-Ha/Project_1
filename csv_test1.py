import pandas as pd

df = pd.read_csv('서울시_지하철_화장실위치_전체.csv')
df1 = pd.read_csv('서울교통공사_역사공중화장실정보_20241127.csv', encoding = 'cp949')

df = df.iloc[1:]

print(df.info())
print(df1.info())

df.to_csv("data.csv", index=False, encoding="utf-8-sig")

print(df.info())