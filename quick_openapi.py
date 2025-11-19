# import requests
# import xml.etree.ElementTree as ET
# import pandas as pd

# SERVICE_KEY = "64427a7971616d69373370496c664f"

# def get_page(start, end):
#     """특정 구간(start~end) 호출해서 item 리스트 반환"""
#     url = f"http://openapi.seoul.go.kr:8088/{SERVICE_KEY}/xml/getFstExit/{start}/{end}/"
#     res = requests.get(url)
#     res.encoding = "utf-8"
#     root = ET.fromstring(res.text)

#     items = root.find("body").find("items")

#     if items is None:
#         return []

#     rows = []
#     for item in items.findall("item"):
#         rows.append({
#             "관리번호": item.findtext("qckgffMngNo"),
#             "호선": item.findtext("lineNm"),
#             "역코드": item.findtext("stnCd"),
#             "역명": item.findtext("stnNm"),
#             "역번호": item.findtext("stnNo"),
#             "기준일자": item.findtext("crtrYmd"),
#             "상하행": item.findtext("upbdnbSe"),
#             "방향(다음역)": item.findtext("drtnInfo"),
#             "칸-문번호": item.findtext("qckgffVhclDoorNo"),
#             "승하차시설": item.findtext("plfmCmgFac"),
#             "시설번호": item.findtext("facNo"),
#             "엘리베이터번호": item.findtext("elvtrNo"),
#             "통로위치": item.findtext("fwkPstnNm"),
#             "시설위치": item.findtext("facPstnNm"),
#         })
#     return rows


# # 전체 페이지 반복
# all_rows = []
# start = 1
# step = 1000

# print("전체 데이터 수집 중...")

# while True:
#     end = start + step - 1
#     print(f"📌 {start} ~ {end} 요청 중...")

#     rows = get_page(start, end)
#     if len(rows) == 0:
#         print("📌 더 이상 데이터 없음 → 종료")
#         break

#     all_rows.extend(rows)
#     start += step

# # DataFrame 만들기
# df = pd.DataFrame(all_rows)
# print("총 데이터 개수:", len(df))

# # CSV 저장
# df.to_csv("전체_빠른승하차정보.csv", index=False, encoding="utf-8-sig")
# print("전체 데이터 CSV 저장 완료!")


import requests
import xml.etree.ElementTree as ET
import pandas as pd

SERVICE_KEY = "64427a7971616d69373370496c664f"  # 네 키

def get_page(start, end):
    """
    getFcRstrm API에서 start~end 구간의 데이터를 받아서
    dict 리스트로 반환
    """
    url = f"http://openapi.seoul.go.kr:8088/{SERVICE_KEY}/xml/getFcRstrm/{start}/{end}/"
    res = requests.get(url)
    res.encoding = "utf-8"

    # 디버깅용 (원본 XML 잠깐 보고싶으면 주석 해제)
    # print(res.text)

    root = ET.fromstring(res.text)

    body = root.find("body")
    if body is None:
        return [], 0

    total_count = int(body.findtext("totalCount", "0") or 0)
    items = body.find("items")

    if items is None:
        return [], total_count

    rows = []
    for item in items.findall("item"):
        rows.append({
            "시설번호": item.findtext("fcltNo"),
            "시설명": item.findtext("fcltNm"),
            "호선": item.findtext("lineNm"),
            "역코드": item.findtext("stnCd"),
            "역명": item.findtext("stnNm"),
            "역번호": item.findtext("stnNo"),
            "기준일자": item.findtext("crtrYmd"),
            "관리번호": item.findtext("mngNo"),
            "출입구내외부": item.findtext("gateInoutSe"),
            "지상지하": item.findtext("grndUdgdSe"),
            "인접출입구번호": item.findtext("vcntEntrcNo"),
            "상세위치": item.findtext("dtlPstn"),
            "화장실정보": item.findtext("rstrmInfo"),
            "역층": item.findtext("stnFlr"),
            "휠체어이용가능": item.findtext("whlchrAcsPsbltyYn"),
        })

    return rows, total_count


# ---------- 메인 로직 ----------
all_rows = []
start = 1
step = 1000  # 한 번에 1000개씩

print("🚽 서울시 지하철 화장실 위치 전체 수집 시작!")

while True:
    end = start + step - 1
    print(f"요청 구간: {start} ~ {end}")

    rows, total_count = get_page(start, end)

    if not rows:
        print("더 이상 데이터가 없습니다. 종료!")
        break

    all_rows.extend(rows)

    # total_count를 넘었으면 종료
    if end >= total_count:
        print("마지막 페이지까지 수집 완료!")
        break

    start += step

# DataFrame 생성
df = pd.DataFrame(all_rows)
print("총 행 개수:", len(df))
print(df.head())

# CSV 저장
out_file = "서울시_지하철_화장실위치_전체.csv"
df.to_csv(out_file, index=False, encoding="utf-8-sig")
print(f"CSV 저장 완료: {out_file}")
