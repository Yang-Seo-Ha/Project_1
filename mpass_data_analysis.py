import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("Mpass_정제.csv")

# 일권별 승차건수 합계
df_sum_total = df['승차건수'].sum() + df['하차건수'].sum()
print(df_sum_total)

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

# print(df_sum)             # 일권별 승차건수 합계   
# print(df_not_zero)            # 일권별 승차 0이 아닌 행 개수 : 추정치 보정값 계산에 필요


# 승차건수 막대그래프 생성
plt.figure(figsize=(10, 6))
plt.bar(df_sum.index, df_sum['승차건수_합계'])

# 라벨 및 제목
plt.xlabel("사용일수구분")
plt.ylabel("승차건수 합계")
plt.title("일권별 승차건수 합계")

# 값 표시
for idx, val in enumerate(df_sum['승차건수_합계']):
    plt.text(idx, val, f"{val:,}", ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()

# 추정치 보정값 계수
df_merged = pd.concat([df_sum, df_not_zero], axis=1)

df_merged['추정치_보정값_계수'] = (df_merged['승차건수_합계'] / df_merged['Not_Zero_Row_Count'])

print(df_merged)


# 판매추정값 구하기
# 날짜 변환 (업무일자 → date)
df['date'] = pd.to_datetime(df['업무일자']).dt.date

# 일수 구분 리스트
pass_list = ["1일권", "2일권", "3일권", "5일권", "7일권"]

result = {}

for p in pass_list:
    # 사용된 날짜 수 (승차건수 != 0 조건)

    coef = df_merged.loc[p, '추정치_보정값_계수']  #[p, '추정치_보정값_계수']

    days_used = (df[
        (df['사용일수구분'] == p) &
        (df['승차건수'] != 0)
    ]['date'].nunique()) * coef
    
    # 숫자만 추출 (예: "7일권" → 7)
    days_total = int(p.replace("일권", ""))
    
    # 판매 추정 = 실제 사용일 수 ÷ 총 이용일수
    sales_est = days_used / days_total
    
    result[p] = {
        "사용된 날짜 수": int(days_used),
        "판매 추정": int(sales_est)
    }

# 출력
for p in pass_list:
    print(f"=== {p} ===")
    print("사용된 날짜 수 :", result[p]["사용된 날짜 수"])
    print("판매 추정 :", result[p]["판매 추정"])
    print()

# x축 레이블(일권), y축 값(판매 추정)
x = list(result.keys())
y = [result[p]["판매 추정"] for p in x]

plt.figure(figsize=(10, 6))
plt.bar(x, y)

plt.title("일권별 판매 추정치")
plt.xlabel("일권")
plt.ylabel("판매 추정")

# 값 표시
for i, val in enumerate(y):
    plt.text(i, val, f"{val:.0f}", ha='center', va='bottom')

plt.tight_layout()
plt.show()


# 일회권 대비 이득 탑승 횟수 계산

# 일권 가격 데이터
data = {
    "일권": ["1일권", "2일권", "3일권", "5일권", "7일권"],
    "가격": [15000, 23000, 30500, 47500, 64500],
    "오후5시_할인가": [12000, 20000, 27500, 44500, 61500]
}

df_price = pd.DataFrame(data)

# 기본 설정
일회권_요금 = 1550
보증금 = 4500

# 순수 이용 비용 계산 (보증금 제외)
df_price["순수_이용비용"] = df_price["가격"] - 보증금

# 몇 번 타야 이득인지 계산 (소수 올림)
df_price["손익분기점_이용횟수"] = df_price["순수_이용비용"].apply(lambda x: math.ceil(x / 일회권_요금))

# 할인 가격도 계산하고 싶다면
df_price["순수_이용비용_할인가"] = df_price["오후5시_할인가"] - 보증금
df_price["손익분기점_할인가"] = df_price["순수_이용비용_할인가"].apply(lambda x: math.ceil(x / 일회권_요금))

# print(df_price)

# x축 위치 정의
labels = df_price["일권"].tolist()
x = np.arange(len(labels))          # [0,1,2,3,4]
width = 0.35                        # 막대 너비

# y값
y_normal = df_price["손익분기점_이용횟수"].values      # 정가 기준
y_discount = df_price["손익분기점_할인가"].values     # 할인가 기준

plt.figure(figsize=(10, 6))

# 막대 두 개씩 나란히
rects1 = plt.bar(x - width/2, y_normal, width, label='정가 기준')
rects2 = plt.bar(x + width/2, y_discount, width, label='할인가 기준')

# 라벨, 제목, 눈금
plt.xticks(x, labels)
plt.xlabel("일권 종류")
plt.ylabel("손익분기점 (이용횟수)")
plt.title("일권별 손익분기점 비교 (정가 vs 오후 5시 이후 할인가)")
plt.legend()

# 막대 위에 값 표시 함수
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, height,
                 f'{int(height)}', ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.tight_layout()
plt.show()


df_price["일수"] = df_price["일권"].str.replace("일권", "").astype(int)

# 정가 기준 하루 손익분기점
df_price["하루_손익분기점"] = df_price["손익분기점_이용횟수"] / df_price["일수"]
df_price["하루_손익분기점"] = df_price["하루_손익분기점"].apply(
    lambda x: math.ceil(x * 10) / 10  # 소수 첫째 자리 올림
)

# 할인가 기준 하루 손익분기점
df_price["하루_손익분기점_할인가"] = df_price["손익분기점_할인가"] / df_price["일수"]
df_price["하루_손익분기점_할인가"] = df_price["하루_손익분기점_할인가"].apply(
    lambda x: math.ceil(x * 10) / 10
)

# ─────────────────────────────
# 2) 그래프 그리기
# ─────────────────────────────
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

labels = df_price["일권"].tolist()
x = np.arange(len(labels))
width = 0.35  # 막대 너비

y_normal = df_price["하루_손익분기점"].values       # 정가 기준
y_discount = df_price["하루_손익분기점_할인가"].values  # 할인가 기준

plt.figure(figsize=(10, 6))

# 막대 두 개씩 나란히
rects1 = plt.bar(x - width/2, y_normal, width, label="정가 기준")
rects2 = plt.bar(x + width/2, y_discount, width, label="할인가 기준")

# 막대 위에 숫자 표시
def autolabel(rects):
    for r in rects:
        h = r.get_height()
        plt.text(r.get_x() + r.get_width()/2, h,
                 f"{h:.1f}", ha="center", va="bottom", fontsize=10)

autolabel(rects1)
autolabel(rects2)

plt.xticks(x, labels)
plt.xlabel("일권 종류")
plt.ylabel("1일 기준 손익분기점 (이용 횟수)")
plt.title("일권별 1일 기준 손익분기점 비교 (정가 vs 오후 5시 이후 할인가)")
plt.legend()
plt.tight_layout()
plt.show()