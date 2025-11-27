import pandas as pd
#데이터 불러오기
df = pd.read_csv('서울교통공사_외국인 관광객 기간권 일별 통행통계_20241231.csv', encoding = 'cp949')

#데이터 일별누적 컬럼 생성
time_cols = [col for col in df.columns if '시' in col]
df['일별누적'] = df[time_cols].sum(axis=1)

#데이터 타입 변경
df['수송일자'] = pd.to_datetime(df['수송일자'])

#언어, 승객유형 분리
df[['언어', '승객유형']] = df['승객유형'].str.split(' ', expand=True)
# 먼저 현재 컬럼 불러오기
cols = list(df.columns)
# 우리가 옮길 열
move_col = '언어'   #  '언어'
# 승객유형 열의 위치 찾기
target_index = cols.index('승객유형')
# move_col 제거
cols.remove(move_col)
# target_index 위치(승객유형 앞)에 다시 삽입
cols.insert(target_index, move_col)
# df 재배치
df = df[cols]


#시간대별 승하차 그래프 그리기
#승차
import matplotlib.pyplot as plt
plt.figure(figsize=(18,8))
time_cols = [c for c in df.columns if c.endswith('시')]
df['월'] = pd.to_datetime(df['수송일자']).dt.month

df_board = df[df['승하차구분'] == '승차']
monthly_hour = df_board.groupby('월')[time_cols].sum()

for month in monthly_hour.index:
    plt.plot(time_cols, monthly_hour.loc[month], marker='o', label=f'{month}월')

plt.xticks(rotation=45)
plt.xlabel("시간대")
plt.ylabel("승차 인원수")
plt.title("월별 시간대별 승차 인원 프로파일")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

#하차
time_cols = [c for c in df.columns if c.endswith('시')]
df['월'] = pd.to_datetime(df['수송일자']).dt.month

df_board = df[df['승하차구분'] == '하차']
monthly_hour = df_board.groupby('월')[time_cols].sum()
import matplotlib.pyplot as plt
plt.figure(figsize=(18,8))

for month in monthly_hour.index:
    plt.plot(time_cols, monthly_hour.loc[month], marker='o', label=f'{month}월')

plt.xticks(rotation=45)
plt.xlabel("시간대")
plt.ylabel("하차 인원수")
plt.title("월별 시간대별 하차 인원 프로파일")
plt.legend()
plt.grid(alpha=0.3)
plt.show()


#호선별 승하차 그래프 그리기
line_sum = df.groupby(['호선', '승하차구분'])['일별누적'].sum().unstack()
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
line_sum.plot(kind='bar', figsize=(10,6))

plt.title("호선별 승차/하차 총합 비교")
plt.xlabel("호선")
plt.ylabel("인원수")
plt.grid(axis='y', alpha=0.3)
plt.xticks(rotation=0)
plt.show()


#외국인 승차가 많은 역

N = 20  # top 개수

board_top = (
    df[df['승하차구분'] == '승차']
    .groupby('역명')['일별누적']
    .sum()
    .sort_values(ascending=False)
    .head(N)
)

plt.figure(figsize=(12,6))
board_top.plot(kind='bar')
plt.title(f"외국인 승차 TOP {N} 역")
plt.xlabel("역명")
plt.ylabel("승차 인원수(일별누적 합)")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

#외국인 하차가 많은 역
N = 20

alight_top = (
    df[df['승하차구분'] == '하차']
    .groupby('역명')['일별누적']
    .sum()
    .sort_values(ascending=False)
    .head(N)
)

plt.figure(figsize=(12,6))
alight_top.plot(kind='bar', color='orange')
plt.title(f"외국인 하차 TOP {N} 역")
plt.xlabel("역명")
plt.ylabel("하차 인원수(일별누적 합)")
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()



#언어에 따른 승하차 역

#승차
langs = df['언어'].unique()
for lang in langs:
    top_board = (
        df[(df['언어'] == lang) & (df['승하차구분'] == '승차')]
        .groupby('역명')['일별누적']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10,5))
    top_board.plot(kind='bar', color='skyblue')
    plt.title(f"{lang} 이용객 — 승차 TOP 10 역")
    plt.ylabel("승차 인원수")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

#하차

for lang in langs:
    top_alight = (
        df[(df['언어'] == lang) & (df['승하차구분'] == '하차')]
        .groupby('역명')['일별누적']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10,5))
    top_alight.plot(kind='bar', color='orange')
    plt.title(f"{lang} 이용객 — 하차 TOP 10 역")
    plt.ylabel("하차 인원수")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


#어린이, 일반 집단 비교하여 비율검정 결과
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

def test_proportion_by_station(df, updown='승차'):
    result = []

    # 1) 승차/하차 필터
    temp = df[df['승하차구분'] == updown]

    # 어린이/일반만
    temp = temp[temp['승객유형'].isin(['어린이','일반'])]

    # 전체 모수
    total_child = temp[temp['승객유형']=='어린이']['일별누적'].sum()
    total_adult = temp[temp['승객유형']=='일반']['일별누적'].sum()

    for station, g in temp.groupby('역명'):

        # 역별 분자
        child_k = g[g['승객유형']=='어린이']['일별누적'].sum()
        adult_k = g[g['승객유형']=='일반']['일별누적'].sum()

        if child_k + adult_k == 0:
            continue

        # 두 비율 검정
        count = [child_k, adult_k]
        nobs  = [total_child, total_adult]

        stat, p = proportions_ztest(count, nobs)

        #  비율 계산
        child_ratio = child_k / total_child if total_child > 0 else 0
        adult_ratio = adult_k / total_adult if total_adult > 0 else 0

        #  어린이가 더 많은지?
        child_more = child_ratio > adult_ratio

        result.append([
            station, child_k, adult_k,
            total_child, total_adult,
            stat, p,
            child_ratio, adult_ratio,
            child_more
        ])

    out = pd.DataFrame(result, columns=[
        '역명',
        '어린이_해당역', '일반_해당역',
        '어린이_전체', '일반_전체',
        'z통계량', 'p값',
        '어린이비율', '일반비율',
        '어린이_더많음'
    ])

    #  p-value < 0.05 유의미 여부 추가
    out['유의미'] = out['p값'] < 0.05

    # p값 기준 정렬
    return out.sort_values('p값')

#수행부분
# ------------------------------------------------------
# 실행
# ------------------------------------------------------

print(" 승차 기준 어린이 vs 일반 비율 차이 검정")
res_up = test_proportion_by_station(df, updown='승차')
print(res_up)

print(" 하차 기준 어린이 vs 일반 비율 차이 검정")
res_down = test_proportion_by_station(df, updown='하차')
print(res_down)
