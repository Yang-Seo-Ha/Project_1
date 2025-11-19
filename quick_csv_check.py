import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('서울교통공사_역사공중화장실정보_20241127.csv', encoding = 'cp949')
print(df.info())

df1 = pd.read_csv('서울시_지하철_화장실위치_전체.csv')
print(df1.info())


# df1 = df1.iloc[1:].reset_index(drop=True)
print(df1.head())
df1.to_csv("정제본_서울시_지하철_화장실위치.csv", index=False)
# # 2) 역명 & 상세위치 추출 (4번째 컬럼 = 역명 / df은 13번째, df1은 11번째)
# df_station = df.iloc[:, 4]
# df_detail   = df.iloc[:, 13].fillna("").astype(str)

# df1_station = df1.iloc[:, 4]
# df1_detail  = df1.iloc[:, 11].fillna("").astype(str)

# # 3) 결과 저장 리스트
# results = []

# # 4) 공통 역명만 비교
# stations = sorted(set(df_station) & set(df1_station))

# for station in stations:
#     # df에서 해당 역
#     a_list = df_detail[df_station == station].tolist()
#     # df1에서 해당 역
#     b_list = df1_detail[df1_station == station].tolist()

#     if len(a_list) == 0 or len(b_list) == 0:
#         continue

#     # TF-IDF 만들기 (역마다 따로 학습)
#     corpus = a_list + b_list
#     vectorizer = TfidfVectorizer()
#     tfidf = vectorizer.fit_transform(corpus)

#     tfidf_a = tfidf[:len(a_list)]
#     tfidf_b = tfidf[len(a_list):]

#     # 유사도 계산
#     sim = cosine_similarity(tfidf_a, tfidf_b)

#     # a_list의 각 항목에 대해 df1 상세위치 중 가장 가까운 것 선택
#     for i, a_text in enumerate(a_list):
#         best_idx = sim[i].argmax()
#         best_score = sim[i].max()
#         b_text = b_list[best_idx]

#         results.append({
#             "역명": station,
#             "교통공사_상세위치": a_text,
#             "서울시_상세위치": b_text,
#             "유사도": best_score
#         })

# # 5) DataFrame 생성
# result_df = pd.DataFrame(results)

# print(result_df.head(20))
# print("평균 유사도:", result_df["유사도"].mean())

