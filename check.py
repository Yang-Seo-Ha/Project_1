import pandas as pd

df = pd.read_csv("Mpass_정제.csv")

order = ["1일권", "2일권", "3일권", "5일권", "7일권"]       # 인덱스 순서

# 일권별 승차건수 합계
df_sum = (
    df[df['승차건수'] != 0]
    .groupby('사용일수구분')['승차건수']
    .sum()
    .reindex(order)
    .to_frame('승차건수_합계')
)

df_not_zero = (
    df[df['승차건수'] != 0]
    .groupby('사용일수구분')['승차건수']
    .count()
    .reindex(order)
    .to_frame('Not_Zero_Row_Count')
)

df_merged = pd.concat([df_sum, df_not_zero], axis=1)

df_merged['평균_승차건수'] = (df_merged['승차건수_합계'] / df_merged['Not_Zero_Row_Count'])

print(df_merged)