import pandas as pd
df = pd.read_csv('전체_빠른승하차정보.csv')
print(df.info())

df1 = pd.read_csv('서울시_지하철_화장실위치_전체.csv')
print(df.head())